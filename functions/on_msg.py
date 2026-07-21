from functions.call_function import call_function
from functions.cutword import cutword
prefix = 'uwu'
async def on_msg(client, message) :
    if message.author == client.user:
        return
    if message.content.lower().startswith(prefix) :
        content = cutword(message.content, prefix)
        print(f"Message:\n{content}\nSent by user:\n{message.author.name}, ID {message.author.id}")
        await call_function(client, message, content)