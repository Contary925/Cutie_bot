import discord
import json
from classes.gif import Gif

class User() :

    def __init__(self, id, name=None):
        self.id = str(id)
        self.name = name
        self.data = self.read_data(self.id)
        self.alias = self.read_alias(self.data)
        self.interactions = self.read_interactions(self.data)
        self.perms = self.read_perms(self.data)
        self.reactions = self.read_reactions(self.data)
        self.responses = self.read_responses(self.data)
        self.favlist = self.read_favlist(self.data) #music favlist

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
        if self.perms == access_level :
            return 0
        self.data_update("perms", access_level)
        self.perms = access_level
        return 1

    def read_reactions(self, data) -> str:
        if not "reactions" in data:
            self.data_update("reactions", {})
        return data["reactions"]

    def read_responses(self, data) -> str:
        if not "responses" in data:
            self.data_update("responses", {})
        return data["responses"]

    def read_favlist(self, data) -> dict :
        if not "favlist" in data:
            self.data_update("favlist", {})
        return data["favlist"]

    def add_to_favlist(self, song: dict):
        if song["url"] in self.favlist:
            return 0
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        data[self.id]["favlist"][song["url"]] = song["title"]
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.favlist[song["url"]] = song["title"]
        self.data["favlist"][song["url"]] = song["title"]
        return 1

    def remove_from_favlist(self, index: int) -> str:
        if index > len(self.favlist):
            return 'Song with index not found'
        url = list(self.favlist)[index-1]
        name = self.favlist[url]
        del self.favlist[url]
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        del data[self.id]["favlist"][url]
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.data_update("favlist", self.favlist)
        return name

    def show_favlist(self) -> str:
        if self.favlist == {}:
            return 'Your favlist is empty!'
        result = ''
        index = 0
        for song_url in self.favlist:
            if index > 20:
                result += 'Cannot display more songs...'
                break
            index += 1
            result += f'{index}. {self.favlist[song_url]}\n'
        return result

                

    def add_reaction(self, text, reaction) :
        if text in self.reactions :
            return 0 
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        data[self.id]["reactions"][text] = reaction
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.reactions[text] = reaction
        self.data_update("reactions", self.reactions)
        return 1

    def add_response(self, text, response) :
            if text in self.responses :
                return 0 
            with open('shared/user_data.json', 'r+') as f:
                data = json.load(f)
            data[self.id]["responses"][text] = response
            with open('shared/user_data.json', 'w') as f:
                json.dump(data, f)
            self.responses[text] = response
            self.data_update("responses", self.responses)
            return 1

    def delete_reaction(self, text) :
        if not text in self.reactions :
            return 0
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        data[self.id]["reactions"].pop(text, None)
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.reactions.pop(text, None)
        self.data_update("reactions", self.reactions)
        return 1

    def delete_response(self, text) :
        if not text in self.responses :
            return 0
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        data[self.id]["responses"].pop(text, None)
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.responses.pop(text, None)
        self.data_update("responses", self.responses)
        return 1
    
    def update_alias(self, alias_key, alias_value) :
        self.read_alias(self.data) #returns nothing, but guaratnees that the alias dict exists
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        data[self.id]["alias"][alias_key] = alias_value
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        self.alias[alias_key] = alias_value
        self.data_update("alias", self.alias)
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

    async def lick(self,  message) :
        url = await self.get_random_gif("lick", message)
        await self.send_embed(message, None, url)

    async def send_embed(self, message, title, url) :
        embed = discord.Embed(
            title=title,
            color =0xE8D1EA,
        )
        embed.set_image(
            url = url
        )
        await message.channel.send(embed = embed)
