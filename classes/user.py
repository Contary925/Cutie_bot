import discord
import json
from classes.gif import Gif

class User() :

    def __init__(self, id, name):
        self.id = str(id)
        self.name = name
        self.data = self.read_data(self.id)
        self.alias = self.read_alias(self.data)
        self.interactions = self.read_interactions(self.data)
        self.perms = self.read_perms(self.data)

    def read_data(self, id) -> dict :
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        if not id in data: #that's a new user! need to initialize data here
            data[id] = {
                "alias" : {},
                "interactions": {},
            }
        with open('shared/user_data.json', 'w') as f:
                json.dump(data, f)
        return data[id]
    
    def data_update(self, key, value) : #a function to use if a key is missing in user data for whatever reason
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        if not key in data[self.id]: 
            data[self.id][key] = value
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.data[key] = value
        
    def read_alias(self, data) -> dict :
        if not "alias" in data :
            self.data_update("alias", {})
        return data["alias"]

    def read_interactions(self, data) -> dict:
        if not "interactions" in data :
            self.data_update("interactions", {})
        return data["interactions"]

    def read_perms(self, data) -> str:
        if not "perms" in data :
            self.data_update("perms", "default")
        return data["perms"]

    def set_perms(self, access_level) :
        self.data_update("perms", access_level)
    
    def update_alias(self, alias_key, alias_value) :
        self.read_alias(self.data) #returns nothing, but guaratnees that the alias dict exists
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        data[self.id]["alias"][alias_key] = alias_value
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.alias[alias_key] = alias_value
        return 1

    def add_interaction(self, other, type) :
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        if not "interactions" in data[self.id] :    
            data[self.id]["interactions"] = {}
        if not type in data[self.id]["interactions"] :
            data[self.id]["interactions"][type] = {}
        if not other.id in data[self.id]["interactions"][type] :
            data[self.id]["interactions"][type][other.id] = 0
        data[self.id]["interactions"][type][other.id] += 1
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.interactions = data[self.id]["interactions"]
        return self.interactions[type][other.id]
    
    def delete_alias(self, alias_key) :
        self.read_alias(self.data) #returns nothing, but guaratnees that the alias dict exists
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        if alias_key in data[self.id]["alias"] :
            del data[self.id]["alias"][alias_key] 
            with open('shared/user_data.json', 'w') as f:
                json.dump(data, f)
            return 1
        return 0

    def check_interaction(self, other, type) :
        if not type in self.interactions :
            return 0
        if not other.id in self.interactions[type] :
            return 0
        return self.interactions[type][other.id]

    async def get_random_gif(self, type, message):
        url = Gif(None, None, type, None).select_random()
        if not url:
            await message.channel.send("Looks like there are no gifs of the specified type. Consider adding some before running this command.")
            return None
        return url
    
    async def hug(self, other, message) :
        url = await self.get_random_gif("hug", message)
        if not url:  #a message already sent by the get_random_gif method
            return
        num_hugs = self.add_interaction(other, "hug")
        if num_hugs == 1 :
            await self.send_embed(message, f"{self.name} hugs {other.name}! That's their first hug!", url)
        else :
            await self.send_embed(message, f"{self.name} hugs {other.name}! That's {num_hugs} hugs now!", url)
    
    async def kiss(self, other, message) :
        url = await self.get_random_gif("kiss", message)
        if not url:
            return
        num_kisses = self.add_interaction(other, "kiss")
        if num_kisses == 1 :
            await self.send_embed(message, f"{self.name} kisses {other.name}! That's their first kiss!", url)
        else :
            await self.send_embed(message, f"{self.name} kisses {other.name}! That's {num_kisses} kisses now!", url)

    async def bite(self, other, message) :
        url = await self.get_random_gif("bite", message)
        if not url:
            return
        num_bites = self.add_interaction(other, "bite")
        if num_bites == 1 :
            await self.send_embed(message, f"{self.name} bites {other.name}! That's their first bite!", url)
        else :
            await self.send_embed(message, f"{self.name} bites {other.name}! That's {num_bites} bites now!", url)

    async def pat(self, other, message) :
        url = await self.get_random_gif("pat", message)
        num_pats = self.add_interaction(other, "pat")
        if num_pats == 1 :
            await self.send_embed(message, f"{self.name} pats {other.name}! That's their first pat!", url)
        else :
            await self.send_embed(message, f"{self.name} pats {other.name}! That's {num_pats} pats now!", url)

    async def spank(self, other, message) :
        num_spanks = self.add_interaction(other, "spank")
        if num_spanks == 1 :
            await message.channel.send(f"{self.name} gave <@{other.id}> a spank! That's their first spank!")
        else :
            await message.channel.send(f"{self.name} gave <@{other.id}> a spank! That's {num_spanks} spanks now!")

    async def send_embed(self, message, title, url) :
        embed = discord.Embed(
            title=title,
            color =0xE8D1EA,
        )
        embed.set_image(
            url = url
        )
        await message.channel.send(embed = embed)
