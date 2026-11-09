# Shell Features

Flux implements a Unix-like command line with familiar shell constructs: piping, redirection, command sequencing, variables, and background processes.

## Command parsing

When you type a line, Flux splits it into tokens using `shlex`-style parsing. The first token (lowercased) is the command name; remaining tokens are arguments. Special characters like quotes and escapes work as expected:

```sh
echo "hello world"        # two tokens: echo, hello world
echo 'path with spaces'   # single argument preserved
```

## Piping (`|`)

The pipe operator connects the **stdout** of one command to the **stdin** of the next. Flux creates temporary files behind the scenes to pass data between commands.

```sh
ls -la | grep ".py"       # list .py files
cat file.txt | wc -l      # count lines in a file
echo hello | cat           # echo → cat
```

Each pipe segment runs as a separate command instance. The last command's stdout goes to the terminal (unless redirected).

## Redirection

Flux supports all standard redirection operators:

| Operator | Meaning |
|----------|---------|
| `>` | Redirect **stdout** to file (overwrite) |
| `>>` | Append **stdout** to file |
| `<` | Read **stdin** from file |
| `<<<` | Feed a string as stdin |
| `<<` | Here-document (multi-line stdin) |
| `2>` | Redirect **stderr** to file |
| `&>` | Redirect **both stdout and stderr** to file |
| `&>>` | Append both stdout and stderr to file |
| `1>` | Explicitly redirect stdout |
| `2>>` | Append stderr |

Examples:

```sh
ls > files.txt              # overwrite files.txt with directory listing
echo "data" >> log.txt      # append to log.txt
cat < input.txt             # read from input.txt as stdin
wc -l < file.txt            # count lines in a file
grep "error" log.txt 2> errors.log    # stderr goes to errors.log
command &> output.txt       # both streams go to output.txt
```

Flux automatically creates parent directories if they don't exist when writing redirected files.

## Command sequencing (`;`)

Semicolons let you run multiple commands in sequence on one line:

```sh
cd /tmp ; mkdir test_dir ; cd test_dir
```

Each segment between semicolons is a separate command pipeline that runs to completion before the next begins.

## Environment variables

Flux maintains its own variable store, populated from the OS environment on startup. Access and set variables with the `$` prefix:

```sh
$HOME          # Your home directory
$PWD           # Current working directory
$PATH          # System PATH (inherited from OS)
$?             # Exit status of the last command (0 = success)
```

Reserved variables (starting with `$`) cannot be deleted. Set new ones using the `export` command:

```sh
export MY_VAR="hello"
echo $MY_VAR
```

### The `$?` variable

After every command, Flux stores its exit status in `$?`:

| Status | Meaning |
|--------|---------|
| `0` | Success (`STATUS_OK`) |
| `1` | Error (`STATUS_ERR`) |
| `2` | Warning (`STATUS_WARN`) |

## Background processes (`&`)

Append `&` to run a command in the background as a separate process:

```sh
sleep 60 &
ps                     # see running background processes
```

Background processes are managed by Flux's internal process manager. Use the `ps` command to list them and `kill` to terminate them.

## Path autocompletion

Press **Tab** to autocomplete file and directory paths at the prompt. Directory names are appended with a trailing `/` for disambiguation.
