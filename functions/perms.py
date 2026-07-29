import functions.call_function
from classes.user import User
from functions.check_owner import check_owner

async def perms(client, message, content) :
    if not await check_owner(message) :
        return
    new_content = "perms_" + content
    #if there's nothing making sense after "alias" then call_function will just pass anyway
    called = await functions.call_function.call_function(client, message, new_content)
    if not called : #if failed to call a function, send instructions :
        await message.channel.send("Usage: perms grant/revoke [user] [access_level]")

async def perms_set(client, message, content) :
    if not await check_owner(message): #this shouldn't be happening, but just to be safe
        return
    args = content.split(' ', maxsplit=1)
    if not len(args) == 2:
        return await message.channel.send("Usage: perms grant/revoke [user] [access_level]")
    [user_mention, access_level] = args
    access_level = access_level.lower()
    if access_level == 'admin' :
        access_level = 'administrator'
    if not access_level in ['default', 'administrator'] :
        return await message.channel.send("Unknown access level. Possible levels are: 'default', 'administrator'.")
    try :
        user_id = user_mention.split("<@")[1].split(">")[0]
    except Exception as e:
        await message.channel.send("Could not find this user! Correctly mention a user. Alias will not work for this command.")
        return 0
    info = await client.fetch_user(user_id)
    user_name = info.display_name  
    user = User(user_id, user_name)
    if not user.set_perms(access_level) :
        return await message.channel.send(f"Failed to change permissions: {user_name} is already a {access_level} user!")
    return await message.channel.send(f"Permissions changed successfully! {user_name} now has {access_level} permissions.")