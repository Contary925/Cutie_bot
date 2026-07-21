import os
import discord
from shared.ID import *
from login import log_in
[client, api_key] = log_in()
from functions.on_msg import on_msg


@client.event
async def on_ready() :
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    await on_msg(client, message)

client.run(api_key)


