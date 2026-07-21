from collections.abc import Callable
from functions.ping import ping
from functions.shutdown import shutdown
import inspect #to decide which parameters are actually needed to a function in the function map

function_map: dict[str, Callable] = {
    "ping" : ping,
    "shutdown": shutdown,
}

async def call_function(client, message, content) :
    command = content.split()[0].lower()
    if command in function_map :
        args = {"client": client, "message": message, "content": content}
        func = function_map[command]
        required_args = {name: args[name] for name in inspect.signature(func).parameters if name in args}
        #which of the args are actually required for the function
        await function_map[command](**required_args)