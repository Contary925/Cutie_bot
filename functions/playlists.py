from classes.user import User
from functions.get_youtube_info import get_youtube_info
from classes.queue import Queue
from functions.music import get_stream_url, play_song
import random
from functions.music import music_queues #warning: this is a global variable!
#it is, however, only being accessed and changed through guild_id keys.
#be careful when mutating it!

async def playlist(client, message, content):
    [command, args] = (content+' ').split(' ', maxsplit=1) #an extra space prevents breaking if there's only one space
    command = command.strip()
    args = args.strip()
    match command:
        case 'create':
            await playlist_create(client, message, args)
        case 'delete':
            await playlist_delete(client, message, args)
        case 'add':
            await add_to_playlist(client, message, args)
        case 'remove':
            await remove_from_playlist(client, message, args)
        case 'play':
            await play_playlist(client, message, args)
        case 'show':
            await show_playlist(client, message, args)
        case 'showall':
            await show_playlists(client, message)
        case _:
            await message.channel.send('Invalid syntax! Usage: uwu playlist [create/delete/add/remove/play] [arguments]. Example: uwu playlist create Three Days Grace')

async def playlist_create(client, message, args):
    user = User(message.author.id)
    match await user.playlist_create(args):
        case True:
            await message.channel.send(f'Successfully created the playlist "{args}"!')
        case False:
            await message.channel.send(f'A playlist "{args}" already exists!')

async def playlist_delete(client, message, args):
    user = User(message.author.id)
    match await user.playlist_delete(args):
        case True:
            await message.channel.send(f'Successfully deleted the playlist "{args}"!')
        case False:
            await message.channel.send(f'No playlist "{args}" found.')

async def add_to_playlist(client, message, args):
    user = User(message.author.id)
    playlists = user.playlists
    for playlist in playlists:
        if playlist in args:
            song_name = args.split(playlist, maxsplit=1)[1]
            break
    if not song_name:
        return await message.channel.send('Incorrect playlist name!')
    song_name = song_name.strip()
    await message.channel.send('Searching for your song...')
    songs = await get_youtube_info(song_name)
    count = 0
    for song in songs:
        count += 1
        await user.add_to_playlist(playlist, song)
    match count:
        case 1:
            title = song["title"]
            return await message.channel.send(f'Added the song **{title}** to playlist **{playlist}**!')
        case _:
            return await message.channel.send(f'Added {count} songs to playlist **{playlist}**!')

async def remove_from_playlist(client, message, args):
    user = User(message.author.id)
    playlists = user.playlists
    for playlist in playlists:
        if playlist in args:
            index = args.split(playlist, maxsplit=1)[1]
            break
    if not index:
        return await message.channel.send('Incorrect playlist name!')
    index = index.strip()
    if not index.isdigit() or int(index) > len(user.playlists[playlist]):
        return await message.channel.send("Invalid index!")
    song_title = await user.remove_from_playlist(playlist, int(index))
    return await message.channel.send(f'Removed the song "{song_title}" from the playlist "{playlist}"!')
    

async def play_playlist(client, message, args):
    shuffle = False
    if args.endswith('-s'):
        shuffle = True
        args = args[:-2].strip()
    user = User(message.author.id)
    if not args in user.playlists:
        return await message.channel.send(f'Cannot find playlist "{args}"!')
    playlist = user.playlists[args]
    if playlist == {}:
        return await message.channel.send(f'The playlist is empty!')
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
    if shuffle:
        songs = list(playlist.items())
        random.shuffle(songs)
        playlist = dict(songs)
    count = 0
    process_message = await message.channel.send('Processing songs in background...')
    for song_url in playlist:
        count += 1
        process_message = await process_message.edit(content=f'Processing songs in background... {count}/{len(playlist)}')
        print(song_url)
        stream_url = await get_stream_url(song_url)
        song = {
            "title": playlist[song_url],
            "url": stream_url
        }
        print(song)
        queue.add(song)
        if count == 1:
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
    await process_message.delete()
    if len(playlist) == 1:
        await message.channel.send(f"Added one song to the queue.")
    else:
        await message.channel.send(f"Added **{len(playlist)} songs** to the queue.")
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


async def show_playlist(client, message, args):
    user = User(message.author.id)
    if not args in user.playlists:
        return await message.channel.send(f'Cannot find playlist "{args}"!')
    playlist = user.playlists[args]
    text = ''
    count = 0
    for song in playlist:
        count += 1
        text += f'{count}. {playlist[song]}\n'
    if count == 0:
        return await message.channel.send(f'The playlist "{args}" is empty!')
    return await message.channel.send(text)

async def show_playlists(client, message):
    user = User(message.author.id)
    text = ''
    count = 0
    for playlist in user.playlists:
        count += 1
        text += f'{count}. **{playlist}**\n'
    if count == 0:
        return await message.channel.send("You don't have any playlists!")
    return await message.channel.send(text)