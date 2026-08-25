import asyncio
from urllib.parse import urlparse, parse_qs
import yt_dlp

# 1. Optimal Configuration (Forcing low quality and light payloads)
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

# 2. Reuse single client instances to save memory and CPU
ydl_client = yt_dlp.YoutubeDL(YTDLP_OPTIONS)

# Create a separate reusable client explicitly for extracting raw video URLs
extract_opts = {**YTDLP_OPTIONS, "extract_flat": False}
ydl_extractor = yt_dlp.YoutubeDL(extract_opts)

async def get_youtube_info(query: str):
    def extract():
        query_str = query.strip()
        
        if query_str.startswith(("http://", "https://")):
            parsed = urlparse(query_str)
            params = parse_qs(parsed.query)
            
            # PLAYLISTS: Fast ID and title extraction using the flat client
            if "list=" in query_str and "v" not in params:
                return ydl_client.extract_info(query_str, download=False)
            
            # SINGLE URLS: Extract actual stream URLs using the deep extractor
            return ydl_extractor.extract_info(query_str, download=False, process=True)
            
        # SEARCH QUERIES: Find the video ID first via the fast flat client
        search_res = ydl_client.extract_info(f"ytsearch1:{query_str}", download=False)
        if search_res and "entries" in search_res and search_res["entries"]:
            video_entry = search_res["entries"][0]
            # Deep extract only this single video to get its low-quality stream URL
            return ydl_extractor.extract_info(video_entry["url"], download=False, process=True)
        return None

    info = await asyncio.to_thread(extract)
    if not info:
        return []

    # Handle Playlist Data (Only triggers for true Playlist URLs now)
    if info.get("_type") == "playlist" and "entries" in info:
        songs = []
        for entry in info["entries"]:
            if entry:
                # Returns clean video watch URLs so they can be extracted when played
                video_id = entry.get("id")
                video_url = entry.get("url") or f"https://youtube.com{video_id}"
                songs.append({
                    "url": video_url, 
                    "webpage_url": video_url,
                    "title": entry.get("title", "Unknown"),
                })
        return songs

    # Pull out the working low-quality stream URL destination
    # Filter through typical yt-dlp keys to grab the raw audio stream link
    stream_url = info.get("url") or (info.get("formats", [{}])[0].get("url") if info.get("formats") else None)
    
    if not stream_url:
        return []

    return [{
        "url": stream_url,
        "webpage_url": info.get("webpage_url") or info.get("url"),
        "title": info.get("title", "Unknown"),
    }]