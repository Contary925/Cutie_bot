async def play(client, message, content):
    if message.author.voice is None:
        message.channel.send("You must be in a voice channel to use this command!")
        return
    channel = message.author.voice.channel
    voice_client = message.guild.voice_client
    if voice_client is not None:
        await voice_client.move_to(channel)
    else:
        voice_client = await channel.connect()


async def stop(client, message, content):
    voice_client = message.guild.voice_client
    if voice_client is not None:
        await voice_client.disconnect()