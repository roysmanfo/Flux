`unzip`
====
Extracts files from compressed zip archives

Syntax
----
```
unzip [-h] [-a] archive_name [destination]
```

Positional Arguments | Description
--------|------------
`archive_name` | the name of the zip archive (you can omit the .zip extension)
`destination` | the destination of the extracted data (default: current directory)

Options | Description
--------|------------
`-h, --help`  | show this help message and exit
`-a, --adapt` | handle conflicts if the destionation folder already exists
