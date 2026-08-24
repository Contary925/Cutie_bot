import json
import discord
from classes.user import User
import functions.call_function

async def send_instructions(message) :
    await message.channel.send("Usage: reply add/remove text_to_reply_to = what_to_reply_with")

async def reply(client, message, content) :
    new_content = "reply_" + content
    called = await functions.call_function.call_function(client, message, new_content)
    if not called : #if failed to call a function, send instructions
        await send_instructions(message)

async def reply_add(message, content) :
    args = content.split("=", maxsplit = 1)
    if not len(args) == 2 :
        await send_instructions(message)
        return
    [text, response_and_args] = args
    if not text or not response_and_args: 
        return await message.channel.send("The text is empty!")
    text = text.strip()
    user = User(message.author.id, None)
    if response_and_args.endswith('all') :
        if not user.perms == "administrator":
            return await message.channel.send("This command can only be executed by an admin.")
        response = response_and_args[:-3].strip()
        with open("shared/responses.json", 'r+') as f:
            responses = json.load(f)
        if text in responses :
            return await message.channel.send(f'There is a response set already to "{text}".')
        responses[text] = response
        with open("shared/responses.json", 'w') as f:
            json.dump(responses, f)
        return await message.channel.send(f'Done! I will now reply with "{response}" to "{text}" in all messages!')
    response = response_and_args.strip()
    if user.add_response(text.lower(), response) :
        return await message.channel.send(f'Done! I will now reply with "{response}" to "{text}" in your messages.')
    else :
        return await message.channel.send(f'There is a reply set already to "{text}"!')

async def reply_remove(message, content) :
    user = User(message.author.id, None)
    if content.endswith('all') :
            if not user.perms == "administrator":
                return await message.channel.send("This command can only be executed by an admin.")
            text = content[:-3].strip()
            with open("shared/responses.json", 'r+') as f:
                responses = json.load(f)
            if not text in responses :
                return await message.channel.send(f'No responses set to "{text}".')
            responses.pop(text, None)
            with open("shared/responses.json", 'w') as f:
                json.dump(responses, f)
            return await message.channel.send(f'Done! No more responses to "{text}".')
    if user.delete_response(content) :
        return await message.channel.send(f'Done! No more responses to "{content}".')
    else :
        return await message.channel.send(f'No responses set to "{content}"!')

async def reply_list(message, content) :
    user = User(message.author.id, message.author.display_name)
    responses = user.responses
    responses_list = f"{user.name}'s responses list: \n"
    for item in responses :
        responses_list += f"{item}: {responses[item]}\n"
    if responses_list == f"{user.name}'s responses list: \n" :
        await message.channel.send("Your responses list is empty!")
    else :
        await message.channel.send(responses_list, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))

async def reply_listall(message, content):
    with open("shared/responses.json", 'r+') as f:
        responses = json.load(f)
    responses_list = f"Global responses list: \n"
    for item in responses :
        responses_list += f"{item}: {responses[item]}\n"
    if responses_list == f"Global responses list: \n" :
        await message.channel.send("The global responses list is empty!")
    else :
        await message.channel.send(responses_list, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
     



async def check_for_replies(message) :
    with open('shared/responses.json', 'r+') as f:
        common_responses = json.load(f)
    for text in common_responses :
        if text in message.content.lower():
            await message.channel.send(common_responses[text], allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))
    with open('shared/user_data.json', 'r+') as f:
        data = json.load(f)
    if not str(message.author.id) in data:
        return #no point in checking for responses if the user never even used the bot
    user = User(message.author.id, None) #the name is unimportant at the moment
    responses = user.responses #a dict of text:response pairs
    for text in responses :
        if text in message.content.lower():
            if user.perms == "administrator" :
                await message.channel.send(responses[text])
            else :
                await message.channel.send(responses[text], allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=False))    
    return