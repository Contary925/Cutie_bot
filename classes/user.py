import discord
import json

class User() :

    def __init__(self, id, name):
        self.id = str(id)
        self.name = name
        self.data = self.read_data(self.id)
        self.alias = self.read_alias(self.data)

    def read_data(self, id) -> dict :
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        if not id in data: #that's a new user! need to initialize data here
            data[id] = {
                "alias" : {}
            }
        with open('shared/user_data.json', 'w') as f:
                json.dump(data, f)
        return data[id]
    
    def data_update(self, key, value) : #a function to use if a key is missing in user data for whatever reason
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        if not key in data[id]: 
            data[id][key] = value
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        
    def read_alias(self, data) -> dict :
        if not "alias" in data :
            self.data_update("alias", {})
        return data["alias"]
    
    def update_alias(self, alias_key, alias_value) :
        self.read_alias(self.data) #returns nothing, but guaratnees that the alias dict exists
        with open('shared/user_data.json', 'r+') as f:
            data = json.load(f)
        data[self.id]["alias"][alias_key] = alias_value
        with open('shared/user_data.json', 'w') as f:
            json.dump(data, f)
        return 1
    
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


    async def hug(self, other, message) :
        url = 'https://media.tenor.com/hacbVpDut3sAAAAM/hug.gif'
        await self.send_embed(message, f"{self.name} hugs {other.name}!", url)
    
    async def kiss(self, other, message) :
        url = 'https://media.tenor.com/kmxEaVuW8AoAAAAd/kiss-gentle-kiss.gif'
        await self.send_embed(message, f"{self.name} kisses {other.name}!", url)

    async def send_embed(self, message, title, url) :
        embed = discord.Embed(
            title=title,
            color = 0xF79AFF,
        )
        embed.set_image(
            url = url
        )
        await message.channel.send(embed = embed)
