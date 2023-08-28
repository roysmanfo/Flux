import shlex


def string_to_list(string: str) -> list[str]:
    # words = string.strip().split(" ")
    # return format(words)
    return shlex.split(string)

def format(words: list[str]) -> list[str]:

    # Items containing a single quote (") each, should be joined as a single item.
    while sigle_quoted_word_exists(words):
        words = join_first_single_quoted_words(words)
    words = [i for i in words if i != '']

    if len(words) > 0:
        words[0] = words[0].lower() if not words[0].startswith("$") else words[0]
    else:
        words.append("")
    return words


def join_first_single_quoted_words(words: list[str]) -> list[str]:
    for word in words:

        if word.count("'") == 1 or word.count("\"") == 1:
            indx = words.index(word)
            words[indx] = " ".join([words[indx], words[indx + 1]])
            words.pop(indx + 1)
            return words


def sigle_quoted_word_exists(words: list[str]) -> bool:
    for word in words:
        if word.count("'") == 1 or word.count("\"") == 1:
            return True
    return False
