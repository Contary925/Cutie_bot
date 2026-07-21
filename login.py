import os
import discord
from dotenv import load_dotenv
from shared.intents import intents

def log_in():
    load_dotenv()
    client = discord.Client(intents=intents)
    api_key = os.environ.get("DISCORD_TOKEN")
    if not api_key :
        raise RuntimeError("Api key not found")
    return client, api_key
