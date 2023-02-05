
def string_to_list(string: str) -> list[str]:
    words = string.strip().split(" ")
    return [i.lower() for i in words]
