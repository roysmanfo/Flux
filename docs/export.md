`export`
====
Allows to create, modify and delete env variables for the current session.    
Once the terminal window is closed, all changes are forgotten and the default settings apply

Syntax
----
```
export [VARIABLE [NEW_VALUE]]
```


Options | Description
--------|------------
`VARIABLE` | The variable to manage (must have $ before: $HOME)
`NEW_VALUE` | The new value of the variable. Lists are rappresented as colon separated values (*val1*:*val2*:*val3*)
