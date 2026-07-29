async def help(message) :
    text = """  Hello! I am Cutie Bot, Kissu's bot for personal use made with discord.py. 
The prefix to use me is '**uwu**' (or '**уву**') - use it every time you want to call me!
Here are some of my commands:
**Interactions**: hug, kiss, pat, bite, boop, lick
**Alias**: alias add, alias remove, alias list
**Gifs**: gif add, gif remove, gif list (remove and add require administrator permissions)
**Misc.**: ping
**Owner only**: shutdown, gitpush, perms set"""
    await message.channel.send(text)