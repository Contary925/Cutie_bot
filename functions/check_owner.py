from shared.ID import OWNER_ID
async def check_owner(message):
    if not message.author.id == OWNER_ID :
        await message.channel.send("Command restricted to be executed by the bot owner only.")
        return 0
    return 1