
def string_to_list(string: str):
    string.strip()
    if string == None or string == '':
        return ['']
    else:
        return decode(string)


def decode(string: str = "") -> list[str]:
    words = []
    for i in string:
        if i == ' ':
            words.append(string[:string.index(i)])
            string = string[string.index(i)+1:]
    words.append(string)
    length = len(words)
    while length > 0:
        if words[length-1] == '':
            words.pop(length-1)
        length -= 1
    words = [i.lower() for i in words]
    return words
