import functions.call_function
from classes.gif import Gif


async def gif(client, message, content):
    called = await functions.call_function.call_function(client, message, 'gif_'+content)
    if not called :
        await message.channel.send("Available functions: gif add, gif remove")

async def gif_add(message, content):
    args = content.split(' ', maxsplit=1)
    if not len(args) == 2 :
        return await message.channel.send("Invalid arguments! Usage: gif add gif_type your_gif_url_here")
    [type, url] = args
    gif = Gif(message, type, url)
    await gif.check()
    if gif_add() :
        return await message.channel.send("Added successfully! (Kidding, just a check)")
    return await message.channel.send("Something went wrong.")

async def gif_remove(message, content):
    pass