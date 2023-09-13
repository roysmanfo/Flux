"""
Always import this module as `fluxcmd`, this will help to bring a certain
consistency in how this module is referenced across all files and reduce
the possible confusion generated from the otherwise overriding of the 
python built-in `cmd` module.

Example:
```py
>>>  from . import cmd as fluxcmd    # correct
>>>  from . import cmd               # not correct
>>>  from . import cmd as cm         # not correct

```
"""

__all__ = [
    'builtin', 
    'export',
    'file',
    'flux',
    'fpm',
    'joke',
    'ls',
    'observer',
    'ps',
    'rm',
    'systemctl',
    'zip'
]

from .builtin import export
from .builtin import file
from .builtin import flux
from .builtin import fpm
from .builtin import joke
from .builtin import ls
from .builtin import observer
from .builtin import ps
from .builtin import rm
from .builtin import systemctl
from .builtin import zip


