import json
from classes.user import User
import functions.call_function

async def send_instructions(message) :
    await message.channel.send("Usage: react add/remove text_to_react_to = emoji_to_react_with")

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
    if not text: #just in case there's completely nothing left
        return await message.channel.send("The text is empty! I cannot react to nothing!")
    while text.startswith(' ') :
        text = text[1:]
    while text.endswith(' ') :
        text = text[:-1]
    #making sure to delete all the excessive spaces that should not be included
    user = User(message.author.id, None) #the name is unimportant - the id is, though.
    #this will be used for permissions check and then for reaction addition
    if reaction_and_args.endswith('all') :
        if not user.perms == "administrator":
            return await message.channel.send("This command can only be executed by an admin.")
        reaction = reaction_and_args[:-3].replace(' ', '')
        if not await check_reaction(message, reaction) :
            return await message.channel.send(f"The provided string {reaction} isn't a valid reaction!")    
        with open("shared/reactions.json", 'r+') as f:
            reactions = json.load(f)
        if text in reactions :
            return await message.channel.send(f'There is a reaction set already to "{text}".')
        reactions[text] = reaction
        with open("shared/reactions.json", 'w') as f:
            json.dump(reactions, f)
        return await message.channel.send(f"Done! I will now react with {reaction} to {text} in all messages!")
    #if the special conditions aren't met, we're just going through the normal react add command
    reaction = reaction_and_args.replace(' ', '') #remove all spaces from the reaction string in case there are any
    if not await check_reaction(message, reaction) : #just making sure the reaction is valid
        return await message.channel.send(f"The provided string {reaction} isn't a valid reaction!")
    if user.add_reaction(text.lower(), reaction) :
        return await message.channel.send(f'Done! I will now react with {reaction} to "{text}" in your messages.')
    else :
        return await message.channel.send(f'There is a reaction set already to "{text}"!')

async def react_remove(message, content) :
    user = User(message.author.id, None)
    if content.endswith('all') :
            if not user.perms == "administrator":
                return await message.channel.send("This command can only be executed by an admin.")
            text = content[:-3]
            while text.startswith(' ') :
                text = text[1:]
            while text.endswith(' ') :
                text = text[:-1]
            with open("shared/reactions.json", 'r+') as f:
                reactions = json.load(f)
            if not text in reactions :
                return await message.channel.send(f'No reactions set to "{text}".')
            reactions.pop(text, None)
            with open("shared/reactions.json", 'w') as f:
                json.dump(reactions, f)
            return await message.channel.send(f'Done! No more reactions to "{text}".')
    if user.delete_reaction(content) :
        return await message.channel.send(f'Done! No more reactions to "{content}".')
    else :
        return await message.channel.send(f'No reactions set to "{content}"!')

async def check_reaction(message, reaction) :
    try :
        await message.add_reaction(reaction)
        return 1
    except Exception :
        return 0
    
async def check_for_reactions(message) :
    with open('shared/reactions.json', 'r+') as f:
        common_reactions = json.load(f)
    for text in common_reactions :
        if text in message.content.lower():
            await message.add_reaction(common_reactions[text])
    with open('shared/user_data.json', 'r+') as f:
        data = json.load(f)
    if not str(message.author.id) in data:
        return #no point in checking for reactions if the user never even used the bot
    user = User(message.author.id, None) #the name is unimportant at the moment
    reactions = user.reactions #a dict of text:reaction pairs
    for text in reactions :
        if text in message.content.lower():
            await message.add_reaction(reactions[text])    
    return
