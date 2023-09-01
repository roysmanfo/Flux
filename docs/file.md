`file`
====
Gets information on a specific file

Syntax
----
```
file [-h] [-m] [-k KEYS] PATH
```

Positional Arguments | Description
--------|------------
`PATH` | The path of the file

Options | Description
--------|------------
`-h, --help` | Show this help message and exit
`-m, --metadata` | Extracts the EXIF metadata of the file if possible.
`-k KEYS, --keys KEYS` | Used combined with `-m`, allows to filter keys (can be used multiple times)
