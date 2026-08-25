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
            
            # PLAYLISTS: Kept separate with extract_flat
            if "list=" in query and "v" not in params:
                playlist_opts = {**YTDLP_OPTIONS, "extract_flat": True}
                with yt_dlp.YoutubeDL(playlist_opts) as ydl:
                    return ydl.extract_info(query, download=False)
            
            # SINGLE VIDEOS: Uses global options (extract_flat is False)
            return ydl_client.extract_info(query, download=False, process=True)
            
        # SEARCH QUERIES: Crucial change here!
        # We explicitly use an isolated downloader call with process=True to 
        # force yt-dlp to fully resolve the direct underlying audio link.
        with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
            return ydl.extract_info(f"ytsearch1:{query}", download=False, process=True)

    info = await asyncio.to_thread(extract)
    if not info:
        return []

    # 1. Handle Playlists (Flat extraction layout)
    if info.get("_type") == "playlist" and "entries" in info and not query.startswith("ytsearch1:"):
        # We check to make sure it's not a text-search playlist
        songs = []
        for entry in info.get("entries", []):
            if entry:
                video_url = entry.get("url") or f"https://www.youtube.com/watch?v={entry['id']}"
                songs.append({
                    "url": video_url, 
                    "webpage_url": video_url,
                    "title": entry.get("title", "Unknown"),
                })
        return songs

    # 2. Handle Search results (When processed, it unwraps the nested entry)
    if "entries" in info:
        entries = info["entries"]
        if not entries:
            return []
        info = entries[0] # Grab the single matching dictionary

    # 3. Handle Single Videos / Resolved Search Links
    # Extract the absolute raw audio link or fall back to webpage_url safely
    stream_url = info.get("url")
    
    return [{
        "url": stream_url,
        "webpage_url": info.get("webpage_url"),
        "title": info.get("title", "Unknown"),
    }]