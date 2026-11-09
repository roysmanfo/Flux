# Built-in Commands

Flux ships with ~50 built-in commands covering file management, system administration, networking, and utility tasks. Below is a reference of the most commonly used ones. For full usage details, run `help <command>` from inside Flux.

## File & Directory

| Command | Description |
|---------|-------------|
| `cat` | Concatenate and print files |
| `echo` | Print arguments to stdout |
| `ls` | List directory contents |
| `mkdir` | Create directories |
| `rm` | Remove files or directories |
| `rmdir` | Remove empty directories |
| `cp` | Copy files/directories |
| `mv` | Move/rename files |
| `touch` | Create empty files or update timestamps |
| `chmod` | Change file permissions |
| `chown` | Change file owner |
| `pwd` | Print working directory |
| `file` | Determine file type |
| `head` | Print first lines of a file |
| `tail` | Print last lines of a file |
| `less` | View file content page by page |
| `grep` | Search files for patterns |

## System

| Command | Description |
|---------|-------------|
| `ps` | List running processes |
| `kill` | Terminate a process |
| `systemctl` | Manage background services |
| `time` | Measure execution time of a command |
| `flux` | Run Flux commands or manage the terminal |
| `settings` | View and edit user settings |
| `export` | Set environment variables |

## Networking

| Command | Description |
|---------|-------------|
| `ping` | Test network connectivity |
| `curl` | Transfer data from/to a server |
| `nc` | Netcat — read/write network connections |
| `ssh` | Secure shell login |
| `ip` | Display network interface information |

## Hashing & Encoding

| Command | Description |
|---------|-------------|
| `md5sum` | Compute MD5 hash |
| `sha1sum` | Compute SHA-1 hash |
| `sha224sum` | Compute SHA-224 hash |
| `sha256sum` | Compute SHA-256 hash |
| `sha512sum` | Compute SHA-512 hash |
| `base64` | Encode/decode base64 data |
| `hex` | Convert between hex and binary |

## Utilities

| Command | Description |
|---------|-------------|
| `help` | List available commands |
| `clear` | Clear the terminal screen |
| `wc` | Count lines, words, characters |
| `observer` | Watch files or directories for changes |
| `itrptctl` | Manage event triggers/interrupts |
| `fpm` | Flux Package Manager — install community commands |
| `joke` | Display a random joke |
| `ext` | Execute external shell commands |
| `unzip` / `zip` | Archive management |

## Redirection & Piping Reference

See [Shell Features](../concepts/shell-features.md) for detailed syntax on:

- Pipes (`|`) — connect command stdout to stdin
- Output redirection (`>`, `>>`, `&>`, etc.)
- Input redirection (`<`, `<<<`, `<<`)
- Command sequencing with semicolons (`;`)
- Background processes with `&`
