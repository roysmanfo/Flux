"""
# `export`
Allows the user to create temporary variables for later use
"""

from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)

class Command(CommandInterface):

    def init(self) -> None:
        self.parser = Parser(prog="export",
                             usage="export name [value] or export -p",
                             description="Set export attribute for shell variables")
        
        self.parser.add_argument("name", nargs="?", help="the exported variable's name")
        self.parser.add_argument("value", nargs="?", help="the value to assign to the variable")
        self.parser.add_argument("-p", action="store_true", help="display a list of all exported variables")
        
    def run(self) -> None:

        if self.args.p or not self.args.name:
            for var in self.system.variables:
                # print the var name without the leading '$'
                self.print(f'declare -x {var.name[1:]}="{var.value}"')
        else:
            self.set_variable()

    def set_variable(self) -> None:
        """
        Create a temporary variable if it doesn't already exist
        or else update it
        """
        name: str = self.args.name
        value = str(self.args.value or "")

        if not name.startswith("$"):
            name = f"${name}"

        if self.system.variables.exists(name):
            self.system.variables.set(name, value.removeprefix("\"").removesuffix("\""))
        else:
            self.system.variables.add(name, value.removeprefix("\"").removesuffix("\""))
        
        self.print()
