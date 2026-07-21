import os
import discord
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("DISCORD_TOKEN")
if not api_key :
    raise RuntimeError("Api key not found")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Ping":
        await message.channel.send('Pong!')

client.run(api_key)

