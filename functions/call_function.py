from collections.abc import Callable
from functions.ping import ping
from functions.shutdown import shutdown
from functions.boop import boop
from functions.interactions import *
from functions.alias import *
from functions.cutword import cutword
from auto_git_push import sync_to_github
import inspect #to decide which parameters are actually needed to a function in the function map

function_map: dict[str, Callable] = {
    "ping" : ping,
    "shutdown": shutdown,
    "hug": hug,
    "kiss": kiss,
    "boop": boop,
    "bite": bite,
    "pat": pat,
    "alias": alias,
    "alias_add": alias_add,
    "alias_remove": alias_remove,
    "alias_list" : alias_list,
    "gitpush" : sync_to_github,
}

function_alias: dict[str, str] = {
    "хаг" : "hug",
    "цем" : "kiss",
    "тык" : "boop",
    "пинг" : "ping",
    "кусь": "bite",
    "ням": "bite",
    "pet" : "pat",
    "пат" : "pat",
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