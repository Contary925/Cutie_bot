from shared.ID import OWNER_ID
from auto_git_push import sync_to_github
async def shutdown(client, message) :
    if message.author.id == OWNER_ID :
        await sync_to_github(message)
        await message.channel.send("Shutting down...")
        await client.close()
    else :
        await message.channel.send("Command restricted to be executed by the bot owner only.")
    