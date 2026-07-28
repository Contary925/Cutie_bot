import functions.call_function
from classes.gif import Gif


async def gif(client, message, content):
    called = await functions.call_function.call_function(client, message, 'gif_'+content)
    if not called :
        await message.channel.send("Available functions: gif add, gif remove")

async def gif_add(message, content):
    url = content
    gif = Gif(message, None, url)
    gif.check()

async def gif_remove(message, content):
    pass