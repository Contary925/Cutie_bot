import asyncio
from urllib.parse import urlparse, parse_qs
import yt_dlp

# 1. High-speed base configuration
YTDLP_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,           # Prevents one dead video from crashing a loop
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
    
    # --- Fast Extraction Flags ---
    "extract_flat": "in_playlist",  # Instantly grabs top-level info without deep parsing
    "skip_download": True,
    "youtube_include_dash_manifest": False,
}

# 2. Reuse ONE global instance to eliminate the setup penalty entirely
ydl_client = yt_dlp.YoutubeDL(YTDLP_OPTIONS)

async def get_youtube_info(query: str):
    def extract():
        if query.startswith(("http://", "https://")):
            parsed = urlparse(query)
            params = parse_qs(parsed.query)
            
            # If it's a direct playlist link, override extract_flat to True
            if "list=" in query and "v" not in params:
                playlist_opts = {**YTDLP_OPTIONS, "extract_flat": True}
                with yt_dlp.YoutubeDL(playlist_opts) as ydl:
                    return ydl.extract_info(query, download=False)
            
            # Single video URL: use the fast global client
            # process=True forces it to resolve the final audio stream URL
            return ydl_client.extract_info(query, download=False, process=True)
            
        # Search query execution
        return ydl_client.extract_info(f"ytsearch1:{query}", download=False)

    # Offload the blocking thread
    info = await asyncio.to_thread(extract)
    if not info:
        return []

    # 3. Handle Playlists (Flat extraction fallback)
    if info.get("_type") == "playlist":
        songs = []
        for entry in info.get("entries", []):
            if entry:
                # Flat extraction doesn't give a direct audio stream 'url' instantly.
                # We provide the direct watch URL, which your player will resolve instantly when it plays.
                video_url = entry.get("url") or f"https://youtube.com{entry['id']}"
                songs.append({
                    "url": video_url, 
                    "webpage_url": video_url,
                    "title": entry.get("title", "Unknown"),
                })
        return songs

    # 4. Handle Search results
    if "entries" in info:
        entries = info["entries"]
        if not entries:
            return []
        info = entries[0]

    # 5. Handle Single Videos
    # yt-dlp puts the streaming audio link in 'url'
    return [{
        "url": info.get("url", info.get("webpage_url")),
        "webpage_url": info.get("webpage_url"),
        "title": info.get("title", "Unknown"),
    }]