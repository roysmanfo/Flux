import shlex
from typing import List, Union

LONG_REDIRECT = ["1>>", "2>>", "&>>", "<<<"]
MEDIUM_REDIRECT = [">>", "<<", "1>", "2>", "&>", "|&"]
SHORT_REDIRECT = [">", "<", "|"]
COMMAND_SEPARATOR = [';']

LM_REDIRECTS = LONG_REDIRECT + MEDIUM_REDIRECT
SHORT_SYMBOLS = SHORT_REDIRECT + COMMAND_SEPARATOR
LOOK_FOR = LM_REDIRECTS + SHORT_SYMBOLS


def string_to_list(string: str) -> List[str]:
    """
    Adapts the list to be used in a shell environment by
    resolving special charachters

    ```
    string_to_list("some text") -> ["some", "text"]
    string_to_list("some 'text in another format'") -> ["some", "text in another format"]
    string_to_list("FIST WORD ALWAYS LOWERCASE") -> ["first", "WORD", "ALWAYS", "LOWERCASE"]
    ```
    """
    try:
        words = shlex.split(string, comments=True, posix=True)
    except ValueError:
        raise
        

    if len(words) > 0:
        words[0] = words[0].lower() if not words[0].startswith("$") else words[0]

        command = []
        for arg in words:
            arg = _separate_redirect_parts(arg)
            command += arg

        return command

    return []

def _separate_redirect_parts(arg: str) -> List[str]:
    """
    This takes as input a string and separates the
    redirect symbol (es. 1> ) from the destination

    ```
    separate_redirect_parts("2>/dev/null") -> ["2>", "/dev/null"]
    separate_redirect_parts("/dev/null") -> ["/dev/null"]
    separate_redirect_parts("ls;pwd") -> ["ls;pwd"]
    """
    
    res = []
    string = ""
    jump = 0
    for i in arg:
        if jump > 0:
            jump -= 1
            continue

        tail = arg[arg.index(i):]
        lm_red = False # long or medium redirect

        for r in LM_REDIRECTS:
            if tail.startswith(r):
                if string:
                    res.append(string)
                string = ""
                res.append(r)
                lm_red = True

                jump = len(r) - 1
                break
            
        if not lm_red: 
            if i in SHORT_SYMBOLS:
                if string:
                    res.append(string)
                    string = ""
                res.append(i)
            else:
                string += i
    
    if string:
        res.append(string)
    
    return res



def split_commands(args: Union[str, List[str]]) -> List[List[str]]:
    """
    This takes as input a string or list of strings and separates the
    diferent commands when a semicolon is found

    ```
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


def split_pipe(args: Union[str, List[str]]) -> List[List[str]] :
    """
    This takes as input a string or list of strings and separates the
    diferent commands when a pipe is found

    ```
    split_commands('echo test| wc') -> [["echo", "test"], ["wc"]]
    split_commands(["echo", "test", "|", "wc"]) -> [["echo", "test"], ["wc"]]
    ```

    Note: this currently works better with a string as input
    """

    if isinstance(args, str):
        args = string_to_list(args)

    res = []
    push = []
    for i in args:
        if i == '|':
            if push:
                res.append(push)
                push = []
        else:
            if i:
                push.append(i)

    if push:
        res.append(push)

    return res
