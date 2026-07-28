import json
import discord
import asyncio

class Gif:
    def __init__(self, client, message, type, url) :
        self.url = url
        self.type = type
        self.gifs = self.read_gifs()
        self.message = message
        self.client = client

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

        def reaction_check(reaction, user): #checking if it's the same message, same person, and a valid reaction
            return (
                user == self.message.author and reaction.message.id == self.message.id 
                and str(reaction.emoji) in ["✅", "❌"]
            )
        try :
            reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=reaction_check)
        except asyncio.TimeoutError:
            await self.message.channel.send("Action declined - no confirmation received.")
        else :
            if str(reaction.emoji) == "✅" :
                try :
                    self.add()
                    await self.message.channel.send("Added successfully!")
                except Exception as e:
                    await self.message.channel.send(f"Failed to add with error: {e}")
            if str(reaction.emoji) == "❌" :
                await self.message.channel.send("Action declined by user.")

    def add(self) :
        pass
    
