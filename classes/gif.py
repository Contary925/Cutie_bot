import json
import discord
import asyncio
import random

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

    async def send(self, title) :
        embed = discord.Embed(
            title=title,
            color =0xE8D1EA,
            )
        embed.set_image(
            url = self.url
        )
        return await self.message.channel.send(embed = embed)

    async def check(self):
        bot_message = await self.send("Is this a valid gif? Confirm by pressing ✅, or decline by pressing ❌.")
        await bot_message.add_reaction("✅")
        await bot_message.add_reaction("❌")

        def reaction_check(reaction, user): #checking if it's the same message, same person, and a valid reaction
            return (
                user == self.message.author and reaction.message.id == bot_message.id 
                and str(reaction.emoji) in ["✅", "❌"]
            )
        try :
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=reaction_check)
        except asyncio.TimeoutError:
            await self.message.channel.send("Action declined - no confirmation received.")
        else :
            if str(reaction.emoji) == "✅" :
                result = self.add()
                await self.message.channel.send(result)
            if str(reaction.emoji) == "❌" :
                await self.message.channel.send("Action declined by user.")

    def add(self) :
        if not self.type in self.gifs :
            self.gifs[self.type] = [] #finally, a list instead of a dict
        if self.url in self.gifs[self.type] :
            return "The gif is already in the list!"
        self.gifs[self.type].append(self.url)
        with open('shared/gifs.json', 'w') as f:
            json.dump(self.gifs, f)
        return "Added successfully!"

    def select_random(self) :
        if not self.type in self.gifs:
            return None
        gifs_list = self.gifs[self.type]
        selected_gif_url = random.choice(gifs_list)
        return selected_gif_url

    async def list(self) :
        if not self.type in self.gifs:
            return await self.message.channel.send("No gifs of this type yet!")
        gifs_list = self.gifs[self.type]
        content = f"Gifs of the {self.type} type:\n"
        for i in range(0, max(len(gifs_list)-1), 19) :
            content += f"{i+1}. {gifs_list[i]}\n"
            if i==19 :
                content += "Cannot list even more..."
        await self.message.channel.send(content)

    
