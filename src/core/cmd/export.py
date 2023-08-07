"""
# `export`
Allows the user to create temporary variables for later use
"""

from .helpers.commands import CommandInterface

class Command(CommandInterface):
    def run(self, command: list, info: object) -> None:
        """
        #### Create/update a variable
        ```
        $ export $var_name new_value
        ```

        #### Access a variable
        ```
        $ $var_name
        ```

        #### Returns

        True if the variable has been set, False otherwise
        """

        # Create a temporary variable if it doesn't already exist
        # else update it
        if len(command) > 2 and command[1].startswith("$") and len(command[1]) > 0:
            self.set_variable(command, info)

    @staticmethod
    def set_variable(command: list, info: object) -> None:
        key: str = command[1].removeprefix("$")
        if key.startswith("$"):
            print("Invalid variable syntax")
            return
        
        value = str(command[2])
        info.variables[key] = value.removeprefix("\"").removesuffix("\"")
        print(f"${key} = {value}")

