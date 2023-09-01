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

__all__ = ['helpers', 'observer', 'flux', 'systemctl', 'joke', 'export', 'ls', 'file', 'ps']

from . import helpers
from . import flux
from . import observer
from . import systemctl
from . import joke
from . import export
from . import ls
from . import file
from . import ps

