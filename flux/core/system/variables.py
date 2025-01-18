from typing import Any, Dict, Iterator, Optional

class Variable:
    def __init__(self, name: str, value: str, is_reserved: bool) -> None:
        self.name = name
        self.value = value
        self.is_reserved = is_reserved

    def __str__(self) -> str:
        return f"Variable(name={self.name}, is_reserved={self.is_reserved}, value={self.value})"

    def __eq__(self, __value: object) -> bool:

        if not isinstance(__value, Variable):
            return False

        return all([__value.name == self.name, __value.value == self.value, __value.is_reserved == self.is_reserved])
    
    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
    
    def copy(self):
        return Variable(self.name, self.value, self.is_reserved)



class Variables:

    def __init__(self):
        self._variables: Dict[str, Variable] = {}

        self.add("$ALL", "$ALL", True)

    def __iter__(self) -> Iterator[Variable]:
        for v in self._variables:
            yield self._variables.get(v)
    
    def __dict__(self):
        res = {}
        for v in self._variables:
            res.update({v: self._variables.get(v).copy()})
        return res

    def add(self, name: str, value: str, is_reserved: bool = False) -> bool:
        """
        Creates a new variable

        `:returns` True if the variable was created, False otherwise (name already taken)
        `:raises` AssertionError if the name provided is not of type str (value instead will be converted in `str(value)`)
        """

        # In case they are provided with the wrong type
        assert isinstance(name, str), "'name' must be of type str "
        value = str(value)
        if self.get(name):
            return False
        
        self._variables.update({name.upper(): Variable(name.upper(), value, is_reserved)})
        self._variables.update({"$ALL": Variable("$ALL", ":".join(sorted(self._variables.keys())), True)})

        return True


    def remove(self, name: str) -> bool:
        """
        Deletes a variable

        Returns True if the variable has been removed, False otherwise (variable not found or is reserved)
        """
        name = name.upper()

        if not self.exists(name):
            return False
        
       
        if self._variables.get(name).is_reserved:
            print(
                f"Variable ${name} can't be deleted because it is a reserved variable")
            return False
        self._variables.pop(name)
        self._variables.update({"$ALL": Variable("$ALL", ":".join(sorted(self._variables.keys())), True)})
        return True

    def exists(self, name: str) -> bool:
        """
        Checks if a variable exists
        """
        for v in self._variables:
            if v == name:
                return True
        return False

    def get(self, name: str, default: Any = None, *, copy: bool = True) -> Optional[Variable]:
        """
        Gets a variable based on its name

        `:param` copy: create a copy of the variable if found

        Returns it's value if the variable has been remove found, otherwise returns default
        """

        v = self._variables.get(name)
        if not v:
            return default
        return v.copy() if copy else v


    def set(self, name: str, value: str) -> None:
        """
        Update the value of a variable
        """

        var = self.get(name, copy=False)

        if not var:
            raise ValueError("invalid key %s" % name)

        var.value = value.__str__()

    def copy(self):
        """
        Creates a screenshot of the current state of env vars (returns a deep copy of all variables) 
        """

        v = Variables()
        for var in self:
            v._variables.update({var.name: var.copy()})
        return v
    
