import discord
import yt_dlp
import asyncio
from classes.queue import Queue
from urllib.parse import urlparse, parse_qs
from classes.user import User
from functions.cutword import cutword
import random

music_queues = {} #warning: this is a global variable!
#it is, however, only being accessed and changed through guild_id keys.
#be careful when mutating it!

YTDLP_OPTIONS = {
    "format": "bestaudio[abr<=128]/bestaudio",
}

async def play(client, message, content):
    match content:
        case "favlist":
            return await play_favlist(message)
        case "favlist -s":
            return await play_favlist(message, shuffle=True)
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
    await message.channel.send("Searching for your song...")
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
    if voice_client.is_playing():
            return
    next_song = queue.next()
    queue.set_current(next_song)
    await play_song(
        voice_client,
        next_song,
        queue,
        message.channel,
    )

async def skip(client, message, auto=False):
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
    if not auto:
        await message.channel.send("Skipping...")
    voice_client.stop()

async def stop(client, message, content):
    voice_client = message.guild.voice_client
    if voice_client is not None:
        await message.channel.send("Stopping...")
        await voice_client.disconnect()
        if message.guild.id in music_queues:
            del music_queues[message.guild.id]
    else:
        await message.channel.send("Currently not playing anything!")

async def show_queue(message):
    guild_id = message.guild.id
    queue = music_queues.setdefault(guild_id, Queue())
    result = queue.show()
    match result:
        case '':
            return await message.channel.send("The queue is empty!")
        case _:
            return await message.channel.send(result)

async def pause(client, message):
    voice_client = message.guild.voice_client
    if voice_client is None or not voice_client.is_playing():
        await message.channel.send("Nothing is currently playing!")
        return
    voice_client.pause()
    await message.channel.send("Paused.")

async def resume(client, message):
    voice_client = message.guild.voice_client
    if voice_client is None or not voice_client.is_paused():
        await message.channel.send("Nothing is currently paused!")
        return
    voice_client.resume()
    await message.channel.send("Resumed.")

async def shuffle(client, message):
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
    queue.shuffle()
    return await message.channel.send("Shuffled successfully!")

async def push(client, message, content, auto=False):
    if (not (content.isdigit() or content == 'last')):
        return await message.channel.send("Incorrect index!")
    if content.isdigit():
        index = int(content)
    else:
        index = 'last'
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
    if index == 'last':
        index = len(queue.songs)+1
    if index < 1:
        return await message.channel.send(f"Incorrect index!")
    if len(queue.songs)+1 < index:
        return await message.channel.send(f"No song number **{index}** in the queue!")
    if index == 2:
        return await message.channel.send(f"Song number **{index}** is already playing next!")
    if index == 1:
        return await message.channel.send(f"This song is already playing!")
    queue.push(index)
    if not auto:
        return await message.channel.send(f"Pushed song number {index} to play next!")

async def playnum(client, message, content):
    await push(client, message, content, auto=True)
    await skip(client, message, auto=True)

async def favlist(message, content):
    if content == '':
        user = User(message.author.id)
        return await message.channel.send(user.show_favlist())
    if content.startswith('add'):
        await add_to_favlist(message, cutword(content, 'add'))
    if content.startswith('remove'):
        await remove_from_favlist(message, cutword(content, 'remove'))

async def add_to_favlist(message, content):
    await message.channel.send("Searching for your song...")
    songs = await get_youtube_info(content)
    if not songs:
        await message.channel.send(
            f"Couldn't find anything for **{content}**."
        )
        return
    song = songs[0]
    user = User(message.author.id)
    match user.add_to_favlist(song):
        case 0:
            return await message.channel.send('The song is already in your favlist!')
        case 1:
            return await message.channel.send(f'Added song **{song["title"]}** to your favlist!')

async def remove_from_favlist(message, content):
    if not content.isdigit():
        return await message.channel.send("Incorrect index! Specify the index of the song in favlist which you want to remove.")
    index = int(content)
    user = User(message.author.id)
    removed = user.remove_from_favlist(index)
    match removed:
        case 'Song with index not found':
            return await message.channel.send("Song with the specified index was not found!")
        case _:
            return await message.channel.send(f"Removed the song **{removed}** from your favlist!")
    

async def play_favlist(message, shuffle=False):
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
    user = User(message.author.id)
    favlist = user.favlist
    if favlist == {}:
        return await message.channel.send('Your favlist is empty!')
    if shuffle:
        songs = list(favlist.items())
        random.shuffle(songs)
        favlist = dict(songs)
    for song_url in favlist:
        song = {
            "url": song_url,
            "title": favlist[song_url]
        }
        queue.add(song)
    if len(favlist) == 1:
        await message.channel.send(f"Added one song to the queue.")
    else:
        await message.channel.send(f"Added **{len(favlist)} songs** to the queue.")
    if voice_client.is_playing():
            return
    next_song = queue.next()
    queue.set_current(next_song)
    await play_song(
        voice_client,
        next_song,
        queue,
        message.channel,
    )

async def repeat(message):
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
    if queue.current_song is None:
        return await message.channel.send("Nothing is currently playing!")
    queue.repeat_current
    return message.channel.send("The current song will play once again!")

#helper functions

async def get_youtube_info(query):
    def extract():
        if query.startswith(("http://", "https://")):
            parsed = urlparse(query)
            params = parse_qs(parsed.query)
            if "v" in params:
                options = {
                    **YTDLP_OPTIONS,
                    "noplaylist": True,
                }
            else:
                options = YTDLP_OPTIONS
            with yt_dlp.YoutubeDL(options) as ydl:
                return ydl.extract_info(query, download=False)
        with yt_dlp.YoutubeDL(YTDLP_OPTIONS) as ydl:
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
            before_options=(
                "-reconnect 1 "
                "-reconnect_streamed 1 "
                "-reconnect_on_network_error 1 "
                "-reconnect_on_http_error 4xx,5xx "
                "-reconnect_delay_max 2"
            ),
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
            "Leaving the voice channel."
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
