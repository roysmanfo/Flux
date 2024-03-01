import shlex
from typing import List, Tuple, Union
import sys as _sys

def string_to_list(string: str) -> List[str]:
    """
    Adapts the list to be used in a shell environment by
    resolving special charachters

    ```py
    string_to_list("some text") -> ["some", "text"]
    string_to_list("some 'text in another format'") -> ["some", "text in another format"]
    string_to_list("FIST WORD ALWAYS LOWERCASE") -> ["first", "WORD", "ALWAYS", "LOWERCASE"]
    ```
    """

    words = shlex.split(string)
    if len(words) > 0:
        words[0] = words[0].lower() if not words[0].startswith("$") else words[0]

        command = []
        for arg in words:
            command += _separate_redirect_parts(arg)

        return command

    return []


def _separate_redirect_parts(arg: str) -> List[str]:
    """
    This takes as input a string and separates the
    redirect symbol (es. 1> ) from the destination

    ```py
    separate_redirect_parts("2>/dev/null") -> ["2>", "/dev/null"]
    separate_redirect_parts("/dev/null") -> ["/dev/null"]
    separate_redirect_parts("ls;pwd") -> ["ls;pwd"]
    """

    # This order is NOT random
    
    LONG_REDIRECT = ["1>>", "2>>", "&>>", "<<<"]
    MEDIUM_REDIRECT = [">>", "<<", "1>", "2>", "&>", "|&"]
    SHORT_REDIRECT = [">", "<", "|"]
    COMMAND_SEPARATOR = [';']

    LOOK_FOR = COMMAND_SEPARATOR + LONG_REDIRECT + MEDIUM_REDIRECT + SHORT_REDIRECT

    for i in LOOK_FOR:
        if arg == i:
            return [i]
        
        if i in COMMAND_SEPARATOR and i in arg:  
            z = arg.split(i)
            res = []
            for j in z:
                res.append(j)
                if j != z[-1]:# or (len(arg) > 0 and arg[-1] == i):
                    res.append(i)

            return res
        elif arg.startswith(i):
            # python 3.8 does not have removeprefix
            if _sys.version_info >= (3, 9):
                return [i, arg.removeprefix(i)]
            return [i, arg[len(i):]]
        
        elif arg.endswith(i):
            # python 3.8 does not have removeprefix
            if _sys.version_info >= (3, 9):
                return [arg.removesuffix(i), i]
            return [-arg[len(i):], i]
        
        
    return [arg] 



def split_commands(args: Union[str, List[str]]) -> List[List[str]]:
    """
    This takes as input a string or list of strings and separates the
    diferent commands when a separator is found semicolon is found

    ```py
    split_commands('echo test; ls') -> [["echo", "test"], ["ls"]]
    split_commands(["echo", "test", ";", "ls"]) -> [["echo", "test"], ["ls"]]
    ```

    Note: this currently works better with a string as input
    """

    if isinstance(args, str):
        args = string_to_list(args)

    res = []
    push = []
    for i in args:
        if i == ";":
            if push:
                res.append(push)
                push = []
        else:
            if i:
                push.append(i)

    if push:
        res.append(push)

    return res

