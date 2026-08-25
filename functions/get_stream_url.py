import asyncio
import yt_dlp

YTDL_OPTS = {
    'format': 'bestaudio/best',
    'skip_download': True,
    'quiet': True,
    'no_warnings': True,
    'nocheckcertificate': True,
    'youtube_include_dash_manifest': False, 
}
ytdl = yt_dlp.YoutubeDL(YTDL_OPTS)

async def get_stream_url(youtube_url: str) -> str | None:
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(
        None, 
        lambda: ytdl.extract_info(youtube_url, download=False)
    )
    return data.get('url')