from shared.ID import OWNER_ID
async def shutdown(client, message) :
    if message.author.id == OWNER_ID :
        await message.channel.send("Shutting down...")
        await client.close()
    else :
        await message.channel.send("Command restricted to be executed by the bot owner only.")
    