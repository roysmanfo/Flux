

def create_table(collumn1: str, collumn2: str, contents: dict) -> str:
    """
    Return a 2 x N table where N rappresents the number of keys in contents
    """

    keys: list[str] = sorted(list(contents.keys()))
    values: list[str] = [contents[i] for i in keys]
    longest_key = 0
    longest_val = 0

    for k in keys:
        longest_key = max(longest_key, len(k))
    for v in values:
        longest_val = max(longest_val, len(str(v)))
    output = ""
    output += f"{collumn1}{' ' * (longest_key - len(collumn1) + 4)}|  {collumn2}\n"
    output += f"{'⎯' * ((longest_key - len(collumn1)) * 2 + 7 + longest_val)}\n"
    for k in keys:
        output += f"{k}{' ' * (longest_key - len(k) + 4)}|  {values[keys.index(k)]}\n"
    output += "\n"

    return output