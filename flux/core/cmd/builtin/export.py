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
        if len(self.command) > 2 and self.command[1].startswith("$") and len(self.command[1]) > 0:
            self.set_variable()

    def set_variable(self) -> None:
        name: str = self.command[1]        
        value = str(self.command[2])
        if self.sysinfo.variables.exists(name):
            self.sysinfo.variables.set(name, value.removeprefix("\"").removesuffix("\""))
        else:
            self.sysinfo.variables.add(name, value.removeprefix("\"").removesuffix("\""))
        
        # Make shure the variable was set
        self.print(f"{name} = '{self.sysinfo.variables.get(name).value}'\n")

