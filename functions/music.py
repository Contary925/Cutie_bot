import discord
import yt_dlp
import asyncio
from classes.queue import Queue

music_queues = {} #warning: this is a global variable!
#it is, however, only being accessed and changed through guild_id keys.
#be careful when mutating it!

YTDLP_OPTIONS = {
    "format": "bestaudio[abr<=128]/bestaudio",
}

async def play(client, message, content):
    if message.author.voice is None:
        await message.channel.send(
            "You must be in a voice channel to use this command!"
        )
        return
    channel = message.author.voice.channel
    voice_client = message.guild.voice_client
    if voice_client is not None:
        await voice_client.move_to(channel)
    else:
        voice_client = await channel.connect()
    guild_id = message.guild.id
    queue = music_queues.setdefault(guild_id, Queue())
    songs = await get_youtube_info(content)
    if not songs:
        await message.channel.send(
            f"Couldn't find anything for **{content}**."
        )
        return
    for song in songs:
        queue.add(song)
    if len(songs) == 1:
        await message.channel.send(f"Added **{songs[0]['title']}** to the queue.")
    else:
        await message.channel.send(f"Added **{len(songs)} songs** to the queue.")
    next_song = queue.next()
    if voice_client.is_playing():
        return
    queue.set_current(song)
    await play_song(
        voice_client,
        next_song,
        queue,
        message.channel,
    )

async def skip(client, message):
    if message.author.voice is None:
        await message.channel.send(
            "You must be in a voice channel to use this command!"
        )
        return
    channel = message.author.voice.channel
    voice_client = message.guild.voice_client
    if voice_client is not None:
        await voice_client.move_to(channel)
    else:
        voice_client = await channel.connect()
    await message.channel.send("Skipping...")
    voice_client.stop()

async def stop(client, message, content):
    voice_client = message.guild.voice_client
    if voice_client is not None:
        await message.channel.send("Leaving the voice channel.")
        await voice_client.disconnect()
    else:
        await message.channel.send("Currently not playing anything!")

async def show_queue(client, message, content):
    guild_id = message.guild.id
    queue = music_queues.setdefault(guild_id, Queue())
    result = queue.show()
    match result:
        case '':
            return await message.channel.send("The queue is empty!")
        case _:
            return await message.channel.send(result)



#helper functions

async def get_youtube_info(query):
    def extract():
        with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
            if query.startswith(("http://", "https://")):
                return ydl.extract_info(query, download=False)
            return ydl.extract_info(
                f"ytsearch1:{query}",
                download=False
            )
    info = await asyncio.to_thread(extract)
    # Playlist
    if info.get("_type") == "playlist":
        songs = []
        for entry in info.get("entries", []):
            if entry:
                songs.append({
                    "url": entry["url"],
                    "title": entry.get("title", "Unknown"),
                })
        return songs
    # Search result
    if "entries" in info:
        entries = info["entries"]
        if not entries:
            return []
        info = entries[0]
    # Single video
    return [{
        "url": info["url"],
        "title": info.get("title", "Unknown"),
    }]

async def play_song(voice_client, song, queue, text_channel):
    source = discord.PCMVolumeTransformer(
        discord.FFmpegPCMAudio(
            song["url"],
            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            options="-vn",
        ),
        volume=0.5,
    )
    loop = asyncio.get_running_loop()
    def playback_finished(error):
        if error:
            print(f"Playback error: {error}")
        asyncio.run_coroutine_threadsafe(
            handle_song_finished(voice_client, queue, text_channel),
            loop,
        )
    voice_client.play(source, after=playback_finished)
    await text_channel.send(
        f"Playing **{song['title']}**"
    )

async def handle_song_finished(voice_client, queue, text_channel):
    next_song = queue.next()
    if next_song is None:
        await text_channel.send(
            "No songs left to play. Leaving the voice channel."
        )
        await voice_client.disconnect()
        return
    queue.set_current(next_song)
    await play_song(
        voice_client,
        next_song,
        queue,
        text_channel,
    )
