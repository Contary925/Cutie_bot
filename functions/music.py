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

async def play(client, message, content, pushing=False):
    shuffle = content.endswith('-s')
    if shuffle:
        content = content[:-2].strip()
    if content == "favlist":
        return await play_favlist(message, shuffle)
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
    if shuffle:
        random.shuffle(songs)
    counter = 0
    for song in songs:
        if pushing:
            queue.insert(counter, song)
            counter += 1
        else:
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

async def queue(message, content):
    if content.startswith('remove'):
        content = cutword(content, 'remove').strip()
        match content:
            case 'last':
                index = 'last'
            case _:
                if not content.isdigit():
                    return
                index = int(content)
        guild_id = message.guild.id
        queue = music_queues.setdefault(guild_id, Queue())
        if index == 'last':
            index = len(queue.songs)+1
        if index < 1:
            return await message.channel.send(f"Incorrect index!")
        if len(queue.songs)+1 < index:
            return await message.channel.send(f"No song number **{index}** in the queue!")
        if index == 1:
            return await message.channel.send(f"This song is already playing! You can use a skip command if you want to skip it.")
        queue.songs.pop(index-2)
        return await message.channel.send(f"Removed song number **{index}** from the queue!")
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
    if content.isdigit():
        index = int(content)
    else:
        match content:
            case 'last':
                index = 'last'
            case _:
                return await play(client, message, content, pushing=True)
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

async def favlist(client, message, content):
    match content:
        case '':
            user = User(message.author.id)
            page = 0
            total_pages = (len(user.favlist) + 19) // 20
            text = user.show_favlist(page)
            sent_message = await message.channel.send(text)
            if total_pages <= 1:
                return
            await sent_message.add_reaction('⬅️')
            await sent_message.add_reaction('➡️')
            def check(reaction, reactor):
                return (
                    reactor.id == message.author.id
                    and reaction.message.id == sent_message.id
                    and str(reaction.emoji) in ('⬅️', '➡️')
                )
            while True:
                try:
                    reaction, reactor = await client.wait_for(
                        'reaction_add',
                        timeout=60.0,
                        check=check
                    )
                except asyncio.TimeoutError:
                    break
                if str(reaction.emoji) == '➡️':
                    if page < total_pages - 1:
                        page += 1
                        await sent_message.edit(
                            content=user.show_favlist(page)
                        )
                elif str(reaction.emoji) == '⬅️':
                    if page > 0:
                        page -= 1
                        await sent_message.edit(
                            content=user.show_favlist(page)
                        )
                await sent_message.remove_reaction(
                    reaction.emoji,
                    reactor
                )
        case 'clear':
            user = User(message.author.id)
            user.clear_favlist()
            return await message.channel.send('Favlist cleared!')
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
    match user.add_to_favlist(
        {
            "url": song["webpage_url"],
            "title": song["title"],
        }
    ):
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
    #it is possible that this command is run by a user rather than
    #automatically, in which case we need to know if they have
    #specified shuffle or not
    if message.content.endswith('-s'):
        shuffle = True
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
    first_iter = True
    for song_url in favlist:
        songs = await get_youtube_info(song_url)
        song = songs[0]
        queue.add(song)
        if first_iter:
            first_iter = False
            if voice_client.is_playing():
                continue
            next_song = queue.next()
            queue.set_current(next_song)
            await play_song(
                voice_client,
                next_song,
                queue,
                message.channel,
            )
            await message.channel.send('Processing songs in background...')

        
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
    queue.repeat_current()
    return await message.channel.send("The current song will play once again!")

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
                    "webpage_url": entry["webpage_url"],
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
        "webpage_url": info["webpage_url"],
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
