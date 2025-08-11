from typing import Callable, Set, Any
from abc import ABCMeta

from flux.utils.exceptions import FluxIllegalOverwrite

# Global set to track method names that shouldn't be overridden
_ILLEGAL_OVERWRITES: Set[str] = set()

def prevent_override(func: Callable) -> Callable:
    """Decorator to mark a method as non-overridable in subclasses."""
    _ILLEGAL_OVERWRITES.add(func.__name__)
    return func

class NoOverrideMeta(ABCMeta):
    """
    Metaclass for classes that have methods that prevent overrides,
    this metaclass should be assigned to the class you are trying to secure, and
    the decorator `prevent_override` should be put on the protected methods

    ```
    class MyClass(metaclass=NoOverrideMeta):
    
        @prevent_override
        def execute(self):
            print('Executing...')

        def validate(self):
            print('Validating...')

            
    class MySubClass(MyClass):
    
        # will not be accepted and will throw an error
        def execute(self):
            print('hacked') 

        # will be accepted
        def validate(self):
            print('Still validating')
            
    ```

    """

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwargs: Any):
        # Check for forbidden overrides
        for method_name in _ILLEGAL_OVERWRITES:
            if method_name in namespace:
                # Find if any base class has this method marked as non-overridable
                for base in bases:
                    if hasattr(base, method_name):
                        original_method = getattr(base, method_name)
                        if method_name in _ILLEGAL_OVERWRITES and callable(original_method):
                            raise FluxIllegalOverwrite(
                                f"Method '{method_name}' is marked as non-overridable "
                                f"and cannot be overridden in class '{name}'."
                            )
        return super().__new__(cls, name, bases, namespace)