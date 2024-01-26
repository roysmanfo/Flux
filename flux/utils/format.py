from typing import Iterator, Any, List, Union


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


def create_adaptive_table(*collumns: Union[str, List[str]], contents: Iterator[Iterator[Any]]) -> str:
    """
    Return a N x M table where N rappresents the number of columns
    and M rappresents the number of records in contents (+2 rows: 1 for the title and 1 for the underline)

    #### Example
    With this input...
    ```
    >>> create_adaptive_table("col1", "col2", contents=[(1, 2), (3, 4)])
    ```

    ... we expect the following output
    ```txt
    col1     col2  
    ----     ------
    1        2  
    3        4  

    ```

    """

    records: list[list[str]] = contents

    n_columns = len(collumns)

    column_widths = [max(len(str(record[i])) for record in records) + 2 for i in range(n_columns)]
    column_widths = [max(len(collumn), width) + 2 for collumn, width in zip(collumns, column_widths)]

    output = ""
    output += "   ".join(f"{collumn}{' ' * (width - len(collumn))}" for collumn, width in zip(collumns, column_widths)) + "\n"
    output += "     ".join("-" * (width - 2) for width in column_widths) + "\n"

    for record in records:
        output += "   ".join(f"{str(record[i])}{' ' * (width - len(str(record[i])))}" for i, width in enumerate(column_widths)) + "\n"

    output += "\n"

    return output

