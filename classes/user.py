import discord
class User() :
    def __init__(self, id, name):
        self.id = id
        self.name = name

    async def hug(self, other, message) :
        url = 'https://media.tenor.com/hacbVpDut3sAAAAM/hug.gif'
        await self.send_embed(message, f"{self.name} hugs {other.name}!", url)
    
    async def kiss(self, other, message) :
        url = 'https://media.tenor.com/kmxEaVuW8AoAAAAd/kiss-gentle-kiss.gif'
        await self.send_embed(message, f"{self.name} kisses {other.name}!", url)

    async def send_embed(self, message, title, url) :
        embed = discord.Embed(
            title=title,
        )
        embed.set_image(
            url = url
        )
        await message.channel.send(embed = embed)
