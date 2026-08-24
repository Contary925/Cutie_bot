import functions.call_function

async def help(client, message, content) :
    new_content = "help_" + content
    called = await functions.call_function.call_function(client, message, new_content)
    if not called : #send default help message
        text = """# Hello! I am **Missu**, Kissu's bot for personal use made with discord.py. 
The prefix to use me is '**uwu**' (or '**уву**') - use it every time you want to call me!
Here are some of my commands:
1. **Interactions**: hug, kiss, pat, bite, boop, lick
2. **Alias**: alias add, alias remove, alias list
3. **Gifs**: gif add, gif remove, gif list (remove and add require administrator permissions)
4. **Reactions**: react add, react remove (react add ... all, react remove ... all - for admins)
5. **Music**: play, stop, pause, push, playnum, repeat, etc. - run "uwu help music" for info!
**Misc.**: ping
**Owner only**: shutdown, gitpush, perms set. 
Try: uwu help [category] for help with specific commands (such as: **uwu help alias**)."""
        await message.channel.send(text)

async def help_alias(message) :
    text = """# Add alias for interactions. 
Examples: 
1. **"uwu alias add Missu = <@1529029241566662746>"**
After this, you will be able to run "uwu spank Missu without actually having to mention me.
Note: you must actually **MENTION** the user to add an alias!
2. "uwu alias remove Missu" - removes an alias.
3. "uwu alias list" - sends the list of all alias you have added."""
    await message.channel.send(text)

async def help_interactions(message) :
    text = """# Interact with a user.
There are quite some interactions, such as: **hug, kiss, pat, bite, spank, boop, lick**, probably more to be added.
For most interactions, the syntax is:
**uwu hug <@1529029241566662746>**
Exceptions: uwu boop, uwu lick
Note: you can use alias instead of mentioning a user. Check "uwu help alias"."""
    await message.channel.send(text)

async def help_gifs(message) :
    text = """# Manage gifs for interactions.
As a default user, you can only view the gifs using gif list:
**uwu gif list hug** (or any other type of interactions).
Admin only commands:
**uwu gif add [type] [url]** - add a new gif to the list of gifs of the specified type.
**uwu gif remove [type] [index]** - remove a gif with the specified intex from the list. View the index using the gif list command."""
    await message.channel.send(text)

async def help_reactions(message) :
    text = """# Manage bot reactions to specific text pieces.
For example:
1. **Uwu react add hello=<:kannahello:983452094432411648>** - this will make me react with <:kannahello:983452094432411648> to every message you send which contains "hello".
2. **Uwu react remove hello** - I will not react to "hello" this way anymore.
Admin only:
3. **Uwu react add hello=<:kannahello:983452094432411648> all** - I will then react with <:kannahello:983452094432411648> to all messages, no matter who sent it.
4. **Uwu react remove hello all** - no more reacting to "hello" in all messages. This **does not** affect other user's set reactions."""
    await message.channel.send(text)

async def help_music(message):
    text = """# Play music from YouTube! Note: you must be in a voice channel to run these commands.
Note: If I'm already playing music, then the "play" command will just add song(s) to the queue.
1. **Uwu play [source]** - play song(s) from a specified source (YouTube search prompt, YouTube video link, or YouTube playlist link)
Example: uwu play Toram Online BGM - King Piton
Note: This might take a while for large playlists!
Specifying a '-s' key will shuffle the songs in playlist (if the source is a YouTube playlist link).
Example: uwu play <https://www.youtube.com/playlist?list=PL43syiOjn5rQ6Bj0EP4CV2fWvCM0WifLD> -s
2. **Uwu pause**, **uwu resume** - pausing/resuming playback. 
**uwu skip** - skipping the current song and playing the next one.
**uwu stop** - stop the playback and delete the queue.
3. **Uwu queue** - view the queue.
4. **Uwu push [index]** - specify a song in queue which you want to play next. 
For example, if the 5th song in queue is "Toram Online BGM - King Piton", then "**uwu push 5**" will make it play next (become number 2 in the queue).
**Uwu push last** will push the last song in the queue instead.
5. **Uwu playnum [index]** - specify a song in queue you want to play right now. The current song will be skipped.
**Uwu playnum last** will play the last song in the queue immediately.
6. **Uwu shuffle** - shuffle the queue.

Run **uwu help favlist** for info about music favlists!"""
    await message.channel.send(text)

async def help_favlist(message):
    text = """# Save songs to your favourite music list and play them quickly and easily!
1. **Uwu favlist** - view your favlist.
2. **Uwu favlist add [source]** - add a song from a specified source to your favlist. Playlists are not supported.
3. **Uwu favlist remove [index]** - remove the song with the specified index from your favlist.
Example: **uwu favlist remove 3** - this will remove the 3rd song from your favlist
4. **Uwu play favlist** - create a queue from your favlist and play it! (Or add everything from your favlist to queue if already playin)
Note: specify a '-s' key to play or add your favlist songs in a random order: **uwu play favlist -s**
Note: **this is faster than using YouTube playlists!**"""
    await message.channel.send(text)