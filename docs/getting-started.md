# Getting Started

This guide walks you through installing Flux and running your first commands.

## Prerequisites

- Python 3.9 or higher (3.10+ recommended)
- pip (Python package manager)

Check your Python version:

```sh
python --version
```

You should see `Python 3.9.x` or higher.

## Installation

### From source

```sh
git clone https://github.com/roysmanfo/Flux.git
cd flux
pip install .
```

After installation, run `flux` from your terminal to start the REPL:

```sh
flux
```

### Development install

If you plan to contribute or modify Flux, work inside a virtual environment:

```sh
python3 -m venv venv
source ./venv/bin/activate    # Linux/macOS
# .\venv\Scripts\activate    # Windows
pip install -r requirements.txt
cd flux && python3 main.py
```

### Running non-interactively

You can pass a command directly as an argument instead of entering the REPL:

```sh
python3 main.py ls /tmp
```

## Your first session

Once you see the prompt:

```
user Flux [version] ~/flux $
```

Try these commands:

```
help               # List all built-in commands
ls                 # List files in the current directory
echo "Hello, Flux" # Print a message
pwd                # Show the current working directory
exit               # Quit the terminal
```

## Directory structure

On first launch Flux creates several folders under `~/.flux/`:

| Path | Purpose |
|------|---------|
| `~/.flux/settings.json` | User settings (username, email, paths) |
| `~/.flux/services.json` | Enabled/disabled services |
| `~/.flux/cache/` | Temporary cache data |
| `~/.flux/.local/` | Local user data |

Temporary files (pipe data, logs, crash reports) live under `/tmp/flux-temp/`.
