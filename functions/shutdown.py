async def shutdown(client, message) :
    await message.channel.send("Shutting down...")
    await client.close()