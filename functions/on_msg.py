from functions.call_function import call_function
from functions.cutword import cutword
from functions.react import check_for_reactions
from functions.reply import check_for_replies

prefix1 = 'uwu'
prefix2 = 'уву'
async def on_msg(client, message) :
    if message.author.bot :
        return
    if message.author == client.user:
        return
    await check_for_reactions(message) #the only thing the bot can do without a prefix - check if the message contains anything
        #it's supposed to react or reply to
    await check_for_replies(message)
    content = None
    if message.content.lower().startswith(prefix1) :
        content = cutword(message.content, prefix1)
    if message.content.lower().startswith(prefix2) :
        content = cutword(message.content, prefix2)
    if content: #only possible if the message starts with a prefix - the bot can do something with the message then.
        #otherwise, it is completely ignored.
        print(f"Message:\n{content}\nSent by user:\n{message.author.name}, ID {message.author.id}")
        await call_function(client, message, content)
    else : #specifically stating this!
        return