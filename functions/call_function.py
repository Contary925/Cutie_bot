from collections.abc import Callable
from functions.ping import ping
from functions.shutdown import shutdown
from functions.interactions import *
from functions.alias import *
from functions.cutword import cutword
from functions.help import *
from functions.gifs import *
from auto_git_push import sync_to_github
from functions.perms import *
from functions.react import react, react_add, react_remove
from functions.reply import reply, reply_add, reply_remove
from functions.music import play, stop, skip, show_queue, shuffle, pause, resume, push, playnum
import inspect #to decide which parameters are actually needed to a function in the function map

function_map: dict[str, Callable] = {
    "ping" : ping,
    "shutdown": shutdown,
    "hug": hug,
    "kiss": kiss,
    "boop": boop,
    "bite": bite,
    "pat": pat,
    "spank": spank,
    "lick": lick,
    "alias": alias,
    "alias_add": alias_add,
    "alias_remove": alias_remove,
    "alias_list" : alias_list,
    "gitpush" : sync_to_github,
    "help" : help,
    "help_alias": help_alias,
    "help_gifs": help_gifs,
    "help_reactions": help_reactions,
    "help_interactions": help_interactions,
    "gif" : gif,
    "gif_add" : gif_add,
    "gif_remove" : gif_remove,
    "gif_list" : gif_list,
    "perms" : perms,
    "perms_set": perms_set,
    "react": react,
    "react_add": react_add,
    "react_remove": react_remove,
    "reply": reply,
    "reply_add": reply_add,
    "reply_remove": reply_remove,
    "play": play,
    "stop": stop,
    "skip": skip,
    "queue": show_queue,
    "shuffle": shuffle,
    "pause": pause,
    "resume": resume,
    "push": push,
    "playnum": playnum,
}

function_alias: dict[str, str] = {
    "хаг" : "hug",
    "цем" : "kiss",
    "кисс" : "kiss",
    "тык" : "boop",
    "пинг" : "ping",
    "кусь": "bite",
    "ням": "bite",
    "pet" : "pat",
    "пат" : "pat",
    "спанк" : "spank",
    "шпаньк" : "spank",
    "лизь" : "lick",
    "гиф" : "gif",
    "gif_адд" : "gif_add",
    "gif_удалить" : "gif_remove",
    "gif_убрать" : "gif_remove",
    "gif_ремув" : "gif_remove",
    "gif_лист" : "gif_list",
    "gif_список" : "gif_list",
    "reaction" : "react",
    "next" : "skip"
}

async def call_function(client, message, content) :
    pre_alias_command = content.split()[0].lower()
    command = pre_alias_command 
    if pre_alias_command in function_alias :
        command = function_alias[command]
    print(f"Processing command: {command}")
    if command in function_map :
        content = cutword(content, pre_alias_command)
        args = {"client": client, "message": message, "content": content}
        func = function_map[command]
        required_args = {name: args[name] for name in inspect.signature(func).parameters if name in args}
        #which of the args are actually required for the function
        await function_map[command](**required_args)
        return 1
    return 0
