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