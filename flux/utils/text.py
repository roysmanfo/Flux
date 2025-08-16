import re


def remove_ansi_escape_sequences(text: str) -> str:
    """
    Remove ANSI escape sequences (color codes and styles) from a given string.

    :param text: a string that may contain ANSI escape sequences
    :return escaped_text: a new string with ANSI escape sequences removed
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
