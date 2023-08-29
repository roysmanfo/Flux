import shlex


def string_to_list(string: str) -> list[str]:
    # words = string.strip().split(" ")
    # return format(words)
    words = shlex.split(string)
    if len(words) > 0:
        words[0] = words[0].lower() if not words[0].startswith("$") else words[0]
        return words
    return [""]
        
