`systemctl`
====
Allows to modify USER settings.  
Settings like `paths` must be provided in this special syntax `set -s path.<path_to_change> -v <new_path>` or `set -s path.<path_to_change> -r`


Syntax
----
```
systemctl [-h] [-s SETTING] [-v VALUE [VALUE ...]] [-r] [--reset-all]
```

Options | Description
--------|------------
`-h, --help` | Show an help message
`-s SETTING` | The setting to change
`-v VALUE` | The new value of the setting to change
`-r, --reset` | Reset the selected setting to it's default value (commbined with -s) 
`--reset-all` | Reset all settings
