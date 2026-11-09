# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Flux** is an extensible, cross-platform Unix-like terminal written in Python (~50 built-in commands: `ls`, `cat`, `grep`, `ssh`, `curl`, `zip`, etc.). It provides a command-line REPL with piping (`|`), redirection (`>`, `>>`, `<`, `<<<`), semicolons, and background processes (`&`).

## Key paths

```
flux/main.py                  # Entry point — REPL loop, readline setup, signal handling
flux/core/_boot.py            # Bootstraps deps/requirements on startup
flux/core/setup.py            # One-line `setup()` that creates System from Settings
flux/core/system/system.py    # Central `System` object — variables, processes, services, privileges
flux/core/manager.py          # Command pipeline: splits commands/pipes/redirections, builds & dispatches
flux/core/interfaces/commands.py  # CommandInterface base class + logging/helpers (the API plugin authors see)
flux/core/system/loader.py    # Dynamic command loading via importlib with LRU cache, search priority chain
flux/core/cmd/builtin/        # Built-in commands (all named <command>.py, default entry point = `Command`)
flux/core/cmd/scripts/        # Custom user-installed commands (searched after builtin)
flux/core/cmd/fpm/            # FPM-package commands (last resort in search chain)
flux/core/services/           # Background services: sys_usage, net_monitor, sys_cleaner, signal_daemon
flux/core/system/interrupts.py  # Signal/event handling & interrupt registration
flux/core/system/variables.py   # Shell-like variable store ($HOME, $PATH, $?, custom vars)
flux/settings/settings.py       # Settings + SysPaths pydantic dataclass hierarchy
flux/utils/parsing.py           # Command parsing: string_to_list(), split_commands(), split_pipe()
flux/utils/exceptions.py        # Custom FluxException types
```

## Development commands

```bash
pip install .                  # Install (or reinstall in-place) from project root
cd flux && python3 main.py     # Run the REPL
python -m unittest tests/*     # Run all unit tests
```

Tests live in `tests/` (`test_shell.py`, `test_utils.py`, `test_variables.py`). The CI workflow (`.github/workflows/run-tests.yml`) runs `pytest` but test files use `unittest.main()` — either runner works.

Commands can also be run non-interactively: `python3 main.py ls /tmp`

## Architecture overview

1. **Boot**: `main.py:main()` → `setup.setup()` creates `System`, then enters the REPL loop.
2. **Input**: User types a command line in `get_line_args()` (colorized prompt via colorama, path autocompletion via readline). Parsed into tokens by `parsing.string_to_list()`.
3. **Pipeline handling**: `manager.run()` splits on `;` for sequencing, detects `|` for piping (creates temp files), parses redirections (`>`, `>>`, `<`, `<<<`, `2>`), and builds command instances via `manager.build()`.
4. **Command loading**: `loader.py` searches directories in priority order (`builtin` → `scripts` → `fpm`). Uses `importlib.import_module` with LRU cache, resolves the entry point class (default `"Command"`, or custom via module-level `ENTRY_POINT`).
5. **Execution**: Each command follows the lifecycle: `init()` → `setup()` (argument parsing) → `run()` (main logic) → `close()` → `exit()`. Exceptions are caught by `fail_safe()` which writes a crash log. Background processes (`&`) go through `system.processes.add()`.
6. **System**: The singleton `System` object holds settings, variables, the interrupt handler, process manager, and service manager.

## Writing commands

Commands are Python files in `flux/core/cmd/builtin/` (or `scripts/`). Minimal structure:

```python
from flux.core.interfaces.commands import CommandInterface, Parser, EventTriggers, Status

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="cmdname", description="...")
        self.parser.add_argument("POSITIONAL", nargs="?")
        self.parser.add_argument("-f", "--flag", action="store_true")

    def run(self):
        self.print("hello from", self.args.POSITIONAL)
```

Key patterns:
- Use `self.print()` / `self.printerr()` for output (respects redirection).
- Use `self.error()`, `self.warning()`, etc. for logging (respect `log_level`).
- Check `self.args` only after `setup()` calls `parser.parse_args()` — the base `setup()` does this automatically.
- Call `super().run()` when overriding — but the base `run()` is abstract, so most commands override it directly.
- For background interruption, register handlers in `init()`: `self.register_interrupt(EventTriggers.SIGINT, target=handler)`.
- Commands can define `PRELOAD_CONFIGS = PreLoadConfigs(prefered_mode_stdout="b")` to change stdin/stdout mode before instantiation.

## Settings & configuration

`Settings` is a pydantic-based hierarchy in `flux/settings/settings.py`. It defines user settings, system paths (where commands/services live), and the version number (read from `flux/settings/version`). On startup, `SysPaths.create_initial_folders()` creates the required directory structure.
