import functions.call_function
from classes.gif import Gif


async def gif(client, message, content):
    called = await functions.call_function.call_function(client, message, 'gif_'+content)
    if not called :
        await message.channel.send("Available functions: gif add, gif remove")

async def gif_add(client, message, content):
    args = content.split(' ', maxsplit=1)
    if not len(args) == 2 :
        return await message.channel.send("Invalid arguments! Usage: gif add gif_type your_gif_url_here")
    [type, url] = args
    if not type in ["hug", "pat", "kiss", "bite"] :
        return await message.channel.send("Wrong gif type!")
    gif = Gif(client, message, type, url)
    await gif.check()

async def gif_list(client, message, content) :
    type = content
    if not type in ["hug", "pat", "kiss", "bite"] :
        return await message.channel.send("Wrong gif type!")
    gif = Gif(client, message, type, None)
    await gif.list()

async def gif_remove(client, message, content):
    args = content.split(' ', maxsplit=1)
    if not len(args) == 2 :
        return await message.channel.send("Invalid arguments! Usage: gif remove gif_type gif_index (check index from the list)")
    [type, index] = args
    if not index.isdigit() :
        return await message.channel.send("Invalid index!")
    index = int(index)
    gif = Gif(client, message, type, None)
    await gif.remove(index)