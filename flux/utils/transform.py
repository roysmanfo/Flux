import shlex
from typing import List
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
    """

    # This order is NOT random
    
    LONG_REDIRECT = ["1>>", "2>>", "&>>", "<<<"]
    MEDIUM_REDIRECT = [">>", "<<", "1>", "2>", "&>", "|&"]
    SHORT_REDIRECT = [">", "<", "|"]

    LOOK_FOR = LONG_REDIRECT + MEDIUM_REDIRECT + SHORT_REDIRECT

    for i in LOOK_FOR:
        if arg.startswith(i):
            if arg == i:
                return [i]
            
            # python 3.8 does not have removeprefix
            if _sys.version_info >= (3, 9):
                return [i, arg.removeprefix(i)]
            return [i, arg[len(i):]]
    return [arg]
