from classes.user import User

async def hug(client, message, content) :
    [id1, name1, id2, name2] = await getinfo(client, message, content)
    user1 = User(id1, name1)
    user2 = User(id2, name2)
    await user1.hug(user2, message)
    
async def kiss(client, message, content) :
    [id1, name1, id2, name2] = await getinfo(client, message, content)
    user1 = User(id1, name1)
    user2 = User(id2, name2)
    await user1.kiss(user2, message)

async def getinfo(client, message, content) :
    id1 = message.author.id
    name1 = message.author.display_name
    try :
        id2 = content.split("<@")[1].split(">")[0]
        info2 = await client.fetch_user(id2)
        name2 = info2.display_name  
        return id1, name1, id2, name2
    except Exception as e:
        await message.channel.send(f"Error: {e}")