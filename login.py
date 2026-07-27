import os
import discord
from dotenv import load_dotenv
from shared.intents import intents

def log_in():
    load_dotenv()
    client = discord.Client(intents=intents)
    api_key = os.environ.get("DISCORD_TOKEN")
    if not api_key:
        raise RuntimeError("Api key not found")

    #special settings for running on WSL1 with Happ. Ignored unless there is a proxy variable set.
    
    system_proxy = (
        os.environ.get("https_proxy") or 
        os.environ.get("HTTPS_PROXY") or 
        os.environ.get("http_proxy") or 
        os.environ.get("HTTP_PROXY")
    )
    
    if system_proxy:
        client.http.proxy = system_proxy
    
    return client, api_key
