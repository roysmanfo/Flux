import os
from typing import Iterable, Any, List, Optional, Union
import re


def create_table(
        *collumns: Union[str, List[str]],
        rows: Iterable[Iterable[Any]],
        show_headers: bool = True,
        fill_value: Optional[Any] = '-',
        separator: str = "-",
        add_top_line: bool = True,
        add_bottom_line: bool = False,
        last_is_footer: bool = False,
    ) -> str:
    """
    Return a N x M table where N rappresents the number of `columns`
    and M rappresents the number of rows in `contents`
    
    ### params 
    - `columns` :             all the column titles
    - `rows` :                the data to populate the table (list of rows)
    - `show_headers` :        when set to false the titles will be discarded in the table
    - `fill_value` :          value to use if there is nothing in that row for this column
    - `separator` :           a character to use to create divisor lines
    - `add_top_line` :        when set to false the line that separates the title from the contents will be omited
    - `add_bottom_line` :     when set to true a line at the end of the table will be added
    - `last_is_footer` :      if set to true, separates the last line from the rest of the table with a divisor 
    
    ### returns
    - `table` :            a new table that satisfies the provided requirements
    
    #### Example
    ```
    >>> create_table("col1", "col2", rows=[(1, 2), (3, 4)])
    ```
    ```txt
    col1     col2  
    ----     ------
    1        2  
    3        4
     
    ```

    ```
    >>> create_table(["col1", "col2"], rows=[(1, 2), (3,)], fill_value="<none>")
    ```
    ```txt
    col1     col2  
    ----     ------
    1        2  
    3        <none>

    """


    if collumns and isinstance(collumns[0], (list, tuple, set)):
        collumns = collumns[0]

    rows: List[List[str]]
    fill_value = str(fill_value or '')

    n_columns = len(collumns)
    
    column_widths = [
        max(
            len(str(record[i]) if i < len(record) else fill_value)
            for record in rows
        ) + 2 for i in range(n_columns)
    ]
    column_widths = [max(len(collumn), width) + 2 for collumn,
                     width in zip(collumns, column_widths)]

    output = ""
    # add the headers
    if show_headers:
        output += "   ".join(f"{collumn}{' ' * (width - len(collumn))}" for collumn, width in zip(collumns, column_widths)) + "\n"
        output += "     ".join((separator if add_top_line else ' ') * (width - 2) for width in column_widths) + "\n"
    
    # add a footer separator
    if last_is_footer:
        rows.insert(-1, tuple((separator if add_top_line else ' ') * (width - 2) for width in column_widths))

    # add all rows (ignores a row's column if there is no header for it)
    for record in rows:
        output += "   ".join(f"{str(record[i]) if i < len(record) else fill_value}{' ' * (width - len(str(record[i]) if i < len(record) else fill_value))}" for i, width in enumerate(column_widths)) + "\n"
    
    # manage footer
    if add_bottom_line:
        output += "     ".join(separator * (width - 2) for width in column_widths) + "\n"
        
    return output

def create_adaptive_table(data: Iterable[str]) -> str:
    """
    Return a dynamically sized table based on the terminal size and the length of the data.

    :param data: an iterable object containing some kind of informations
    :returns table: a string representing the formatted table
    """

    if len(data) == 0:
        return ""
    
    terminal_width = os.get_terminal_size().columns
    longest = len(data[0])

    for d in data:
        cell = remove_ansi_escape_sequences(d.__str__())
        longest = max(longest, len(cell))

    num_columns = max(1, terminal_width // longest)
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

    :param text: a string that may contain ANSI escape sequences
    :return escaped_text: a new string with ANSI escape sequences removed
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
