
class Variable:
    def __init__(self, name: str, value: str, is_reserved: bool) -> None:
        self.name = name
        self.value = value
        self.is_reserved = is_reserved

    def __str__(self) -> str:
        return f"Variable(name={self.name}, is_reserved={self.is_reserved}, value={self.value})"


class Variables:

    def __init__(self) -> None:
        self.variables: list[Variable] = []

    def add(self, name: str, value: str, is_reserved: bool = False) -> None:
        """
        Creates a new variable
        """
        self.variables.append(Variable(name, value, is_reserved))

    def remove(self, name: str) -> bool:
        """
        Deletes a variable

        Returns True if the variable has been removed, False otherwise (variable not found)
        """
        for var in self.variables:
            if var.name == name:
                if var.is_reserved:
                    print(
                        f"Variable ${var.name} can't be deleted because it is a reserved variable")

                self.variables.remove(var)
                return True

        return False

    def exists(self, name: str) -> bool:
        """
        Checks if a variable exists
        """
        for var in self.variables:
            if var.name == name:
                return True

        return False

    def get(self, name: str) -> Variable | None:
        """
        Gets the value of a variable

        Returns it's value if the variable has been remove found, None otherwise
        """
        for var in self.variables:
            if var.name == name:
                return var

        return None

    def set(self, name: str, value: str) -> None:
        """
        Update the value of a variable
        """
        for var in self.variables:
            if var.name == name:
                var.value = str(value)
                return

    def no_var_found(self, var):
        """
        Should be called when a variable with specified name is found
        """
        print(f"No variable ${var} found")
