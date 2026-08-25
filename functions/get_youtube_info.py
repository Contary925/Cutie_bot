import asyncio
from urllib.parse import urlparse, parse_qs
import yt_dlp

# 1. Base Configuration
YTDLP_OPTIONS = {
    "format": "worstaudio/worst[ext=webm]/worst", 
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,           
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",
    "skip_download": True,
    "extract_flat": "in_playlist", 
    "youtube_include_dash_manifest": False,
    "youtube_include_hls_manifest": False, 
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "ios"], 
            "skip": ["dash", "hls"] 
        }
    },
}

# Pre-instantiate these globally once to save CPU and RAM cycles
ydl_client = yt_dlp.YoutubeDL(YTDLP_OPTIONS)
ydl_playlist_client = yt_dlp.YoutubeDL({**YTDLP_OPTIONS, "extract_flat": True})
ydl_search_client = yt_dlp.YoutubeDL({
    **YTDLP_OPTIONS,
    "extract_flat": False,       
    "playlist_items": "1",       
    "youtube_include_dash_manifest": False, 
    "youtube_include_nsig_html": False,     
})

async def get_youtube_info(query: str):
    def extract():
        if query.startswith(("http://", "https://")):
            parsed = urlparse(query)
            params = parse_qs(parsed.query)
            
            # PLAYLISTS
            if "list=" in query and "v" not in params:
                return ydl_playlist_client.extract_info(query, download=False)
            
            # SINGLE URLS
            return ydl_client.extract_info(query, download=False, process=True)
            
        # SEARCH QUERIES
        return ydl_search_client.extract_info(f"ytsearch1:{query}", download=False, process=True)

    info = await asyncio.to_thread(extract)
    if not info:
        return []

    # Handle containers
    if info.get("_type") == "playlist" and "entries" in info:
        entries = info["entries"]
        if not entries:
            return []
        
        # FIX 1: If it came from search, entries[0] contains the actual data
        if not query.startswith(("http://", "https://")):
            info = entries[0] 
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

    # FIX 2: Safely extract stream URL even if nested inside yt-dlp's formats block
    stream_url = info.get("url")
    if not stream_url and info.get("formats"):
        stream_url = info["formats"][0].get("url")
        
    if not stream_url:
        stream_url = info.get("webpage_url")
    
    return [{
        "url": stream_url,
        "webpage_url": info.get("webpage_url"),
        "title": info.get("title", "Unknown"),
    }]