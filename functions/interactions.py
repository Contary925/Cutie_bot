from classes.user import User

async def hug(client, message, content) :
    info = await getinfo(client, message, content)
    if not info :
        return 0
    [id1, name1, id2, name2] = info
    user1 = User(id1, name1)
    user2 = User(id2, name2)
    await user1.hug(user2, message)
    
async def kiss(client, message, content) :
    info = await getinfo(client, message, content)
    if not info :
        return 0
    [id1, name1, id2, name2] = info
    user1 = User(id1, name1)
    user2 = User(id2, name2)
    await user1.kiss(user2, message)

async def bite(client, message, content) :
    info = await getinfo(client, message, content)
    if not info :
        return 0
    [id1, name1, id2, name2] = info
    user1 = User(id1, name1)
    user2 = User(id2, name2)
    await user1.bite(user2, message)

async def pat(client, message, content) :
    info = await getinfo(client, message, content)
    if not info:
        return 0
    [id1, name1, id2, name2] = info
    user1 = User(id1, name1)
    user2 = User(id2, name2)
    await user1.pat(user2, message)

async def getinfo(client, message, content) :
    id1 = message.author.id
    name1 = message.author.display_name
    user1 = User(id1, name1)
    if content in user1.alias :
        content = user1.alias[content]
    try :
        id2 = content.split("<@")[1].split(">")[0]
    except Exception as e:
        await message.channel.send("Could not find this user! Correctly mention a user or use alias.")
        return 0
    info2 = await client.fetch_user(id2)
    name2 = info2.display_name  
    return id1, name1, id2, name2