from functions.call_function import call_function
from functions.cutword import cutword
prefix1 = 'uwu'
prefix2 = 'уву'
async def on_msg(client, message) :
    if message.author == client.user:
        return
    content = None
    if message.content.lower().startswith(prefix1) :
        content = cutword(message.content, prefix1)
    if message.content.lower().startswith(prefix2) :
        content = cutword(message.content, prefix2)
    if content: #only possible if the message starts with a prefix
        print(f"Message:\n{content}\nSent by user:\n{message.author.name}, ID {message.author.id}")
        await call_function(client, message, content)