import os
from typing import Iterable, Any, List, Union
import re


def create_table(*collumns: Union[str, List[str]], contents: Iterable[Iterable[Any]], show_headers: bool = True) -> str:
    """
    Return a N x M table where N rappresents the number of columns
    and M rappresents the number of records in contents (+2 rows: 1 for the title and 1 for the underline)

    #### Example
    With this input...
    ```
    >>> create_table("col1", "col2", contents=[(1, 2), (3, 4)])
    ```

    ... we expect the following output
    ```txt
    col1     col2  
    ----     ------
    1        2  
    3        4  

    ```

    """

    if collumns and isinstance(collumns[0], (list, tuple, set)):
        collumns = collumns[0]
    records: List[List[str]] = contents

    n_columns = len(collumns)

    column_widths = [max(len(str(record[i])) for record in records) + 2 for i in range(n_columns)]
    column_widths = [max(len(collumn), width) + 2 for collumn, width in zip(collumns, column_widths)]

    output = ""
    if show_headers:
        output += "   ".join(f"{collumn}{' ' * (width - len(collumn))}" for collumn, width in zip(collumns, column_widths)) + "\n"
        output += "     ".join("-" * (width - 2) for width in column_widths) + "\n"

    for record in records:
        output += "   ".join(f"{str(record[i])}{' ' * (width - len(str(record[i])))}" for i, width in enumerate(column_widths)) + "\n"

    output += "\n"

    return output

def create_adaptive_table(data: Iterable[str]) -> str:
    """
    Return a dynamically sized table based on the terminal size and the length of the data.

    `:param data` : an iterable object containing some kind of informations
    `:returns` : a string representing the formatted table
    """

    if len(data) == 0:
        return ""
    
    terminal_width = os.get_terminal_size().columns
    longest = len(data[0])

    for d in data:
        cell = remove_ansi_escape_sequences(d.__str__())
        longest = max(longest, len(cell))

    num_columns = max(1, terminal_width // longest)  # Adjust this value based on your preference
    num_rows = (len(data) + num_columns - 1) // num_columns

    output = ""

    for row in range(num_rows):
        start_index = row * num_columns
        end_index = min((row + 1) * num_columns, len(data))
        row_data = data[start_index:end_index]
        output += " ".join(str(item).ljust(longest) for item in row_data) + "\n"

    return output


def remove_ansi_escape_sequences(text: str) -> str:
    """
    Remove ANSI escape sequences (color codes and styles) from a given string.

    `:param text` : a string that may contain ANSI escape sequences
    `:return` : a new string with ANSI escape sequences removed
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
