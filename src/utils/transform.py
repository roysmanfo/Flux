import shlex


def string_to_list(string: str) -> list[str]:
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
        return words
    return []
        
