import json
from classes.user import User
import functions.call_function
from functions import check_owner

async def send_instructions(message) :
    await message.channel.send("Usage: react add/remove text_to_react_to emoji_to_react_with")

async def react(client, message, content) :
    new_content = "react_" + content
    called = await functions.call_function.call_function(client, message, new_content)
    if not called : #if failed to call a function, send instructions
        await send_instructions(message)

async def react_add(message, content) :
    args = content.split('=', maxsplit=1)
    if not len(args) == 2 :
        await send_instructions(message)
        return
    [text, reaction_and_args] = args #reaction and args is supposed to be either just the reaction, or reaction + "all"
    reaction_and_args_split = reaction_and_args.split(' ', maxsplit=1)
    if len(reaction_and_args_split) == 2 :
        if reaction_and_args_split[1] == 'all' : #quite specific conditions for the admin only command
            if not await check_owner(message) :
                return await message.channel.send("React add all command not yet implemented.") #TODO
    #if the special conditions aren't met, we're just going through the normal react add command
    reaction = reaction_and_args_split[0].replace(' ', '') #remove all spaces from the reaction string in case there are any
    while text.startsWith(' ') :
        text = text[1:]
    while text.endsWith(' ') :
        text = text[:-1]
    #making sure to delete all the excessive spaces that should not be included
    if not text: #just in case there's completely nothing left
            return await message.channel.send("The text is empty! I cannot react to nothing!")
    if not await check_reaction(message, reaction) : #just making sure the reaction is valid
        return await message.channel.send(f"The provided string {reaction} isn't a valid reaction!")
    user = User(id, None) #the name is unimportant - the id is, though
    user.add_reaction(text, reaction)

async def check_reaction(message, reaction) :
    try :
        await message.add_reaction(reaction)
        return 1
    except Exception :
        return 0
    
    

