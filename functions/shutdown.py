from shared.ID import OWNER_ID
from auto_git_push import sync_to_github
from functions.check_owner import check_owner
async def shutdown(client, message) :
    if await check_owner(message) :
        await sync_to_github(message)
        await message.channel.send("Shutting down...")
        await client.close()
        
    