import json
import discord

class Gif:
    def __init__(self, message, type, url) :
        self.url = url
        self.type = type
        self.gifs = self.read_gifs()
        self.message = message

    def read_gifs(self) :
        with open('shared/gifs.json', 'r+') as f:
            gifs = json.load(f)
        return gifs

    async def check(self):
        embed = discord.Embed(
             title="Is this a valid gif? Confirm by pressing ✅, or decline by pressing ❌.",
            color =0xE8D1EA,
        )
        embed.set_image(
            url = self.url
        )
        bot_message = await self.message.channel.send(embed = embed)
        await bot_message.add_reaction("✅")
        await bot_message.add_reaction("❌")

    async def add(self) :
        pass
    
