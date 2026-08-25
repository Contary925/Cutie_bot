import asyncio
from urllib.parse import urlparse, parse_qs
import yt_dlp

# 1. Base Configuration (No global extract_flat!)
YTDLP_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,           
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
    
    # Safe Speed flags
    "skip_download": True,
    "youtube_include_dash_manifest": False,
    "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
}

ydl_client = yt_dlp.YoutubeDL(YTDLP_OPTIONS)

async def get_youtube_info(query: str):
    def extract():
        if query.startswith(("http://", "https://")):
            parsed = urlparse(query)
            params = parse_qs(parsed.query)
            
            # PLAYLISTS: Fast ID and title extraction
            if "list=" in query and "v" not in params:
                playlist_opts = {
                    **YTDLP_OPTIONS, 
                    "extract_flat": True
                }
                with yt_dlp.YoutubeDL(playlist_opts) as ydl:
                    return ydl.extract_info(query, download=False)
            
            # SINGLE URLS
            return ydl_client.extract_info(query, download=False, process=True)
            
        # SEARCH QUERIES: Stripping out heavy assets on the fly
        search_opts = {
            **YTDLP_OPTIONS,
            "extract_flat": False,       # Allow it to resolve the stream URL...
            "playlist_items": "1",       # ...but strictly stop after the 1st match
            "youtube_include_dash_manifest": False, # Bypasses heavy manifest parsing
            "youtube_include_nsig_html": False,     # Disables heavy client JS rendering
        }
        with yt_dlp.YoutubeDL(search_opts) as ydl:
            return ydl.extract_info(f"ytsearch1:{query}", download=False, process=True)

    info = await asyncio.to_thread(extract)
    if not info:
        return []

    # Handle containers
    if info.get("_type") == "playlist" and "entries" in info:
        entries = info["entries"]
        if not entries:
            return []
        
        # If it came from our text search block
        if query.startswith("ytsearch1:") or not query.startswith(("http://", "https://")):
            info = entries[0] # Grab the fully processed song object
        else:
            # Explicit playlist URL link mapping
            songs = []
            for entry in entries:
                if entry:
                    video_url = entry.get("url") or f"https://youtube.com{entry['id']}"
                    songs.append({
                        "url": video_url, 
                        "webpage_url": video_url,
                        "title": entry.get("title", "Unknown"),
                    })
            return songs

    # Pull out the working stream URL destination
    stream_url = info.get("url") or info.get("webpage_url")
    
    return [{
        "url": stream_url,
        "webpage_url": info.get("webpage_url"),
        "title": info.get("title", "Unknown"),
    }]