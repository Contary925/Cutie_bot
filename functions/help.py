async def help(message) :
    text = """  Hello! I am Cutie Bot, Kissu's bot for personal use written using discord.py. 
The prefix to use me is 'uwu' (or 'уву') - use it every time you want to call me!
Here are some of my commands:
Interactions: hug, kiss, pat, bite
Alias: alias add, alias remove, alias list
Misc.: ping, boop
Owner only: shutdown, gitpush"""
    await message.channel.send(text)