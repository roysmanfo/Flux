"""
# `export`
Allows the user to create temporary variables for later use
"""

from flux.core.helpers.commands import CommandInterface

class Command(CommandInterface):
    def run(self) -> None:
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
        if len(self.line_args) > 2 and self.line_args[1].startswith("$") and len(self.line_args[1]) > 0:
            self.set_variable()

    def set_variable(self) -> None:
        name: str = self.line_args[1]        
        value = str(self.line_args[2])
        if self.system.variables.exists(name):
            self.system.variables.set(name, value.removeprefix("\"").removesuffix("\""))
        else:
            self.system.variables.add(name, value.removeprefix("\"").removesuffix("\""))
        
        # Make shure the variable was set
        self.print(f"{name} = '{self.system.variables.get(name).value}'\n")

