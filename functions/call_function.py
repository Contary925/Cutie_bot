from shared.ID import *
from collections.abc import Callable
from functions.ping import ping
from functions.shutdown import shutdown
async def call_function(client, message, content) :
    if content.lower() == "ping":
        await ping(message)
    if content.lower() == "shutdown" :
        if message.author.id == OWNER_ID :
            await shutdown(client, message)
        else :
            await message.channel.send("Command restricted to be executed by the bot owner only.")