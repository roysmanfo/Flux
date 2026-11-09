# System & Variables

## The System object

The `System` singleton is the central hub of Flux. Every command receives a reference to it as `self.system`. It holds:

| Attribute | Type | Description |
|-----------|------|-------------|
| `settings` | `Settings` | User settings and system paths |
| `version` | `str` | Current Flux version |
| `privileges` | `Privileges` (enum) | Privilege levels: `LOW`, `HIGH`, `SYSTEM` |
| `interrupt_handler` | `InterruptHandler` | Signal and event registration |
| `variables` | `Variables` | Shell-like variable store |
| `processes` | `Processes` | Background process manager |
| `service_manager` | `Servicemanager` | Lifecycle management for background services |

### Privileges

Commands can run at different privilege levels:

- **LOW** — default for all user commands
- **HIGH** — elevated access (reserved for specific system commands)
- **SYSTEM** — full system access

A command can check its own privileges via `self.has_high_priv` and `self.has_sys_priv`.

## Variables

Flux's variable store is implemented by the `Variables` class. Variables are keyed by name with a `$` prefix (e.g., `$HOME`). Each variable has a name, value, and a reserved flag.

### Built-in variables

| Variable | Description |
|----------|-------------|
| `$ALL` | Colon-separated list of all variable names (reserved) |
| `$HOME` | User's home directory |
| `$PATH` | System PATH from the OS environment |
| `$PWD` | Current working directory |
| `$OLDPWD` | Previous working directory |
| `$?` | Exit status of the last command |
| `$<OS_VAR>` | All environment variables inherited from the OS |

### Variable API

```python
# In a command, access via self.system.variables:

self.system.variables.add(name, value, is_reserved=False)   # Create a new variable; returns True/False
self.system.variables.remove(name)                           # Delete (fails if reserved); returns True/False
self.system.variables.exists(name)                           # Check existence; returns bool
self.system.variables.get(name, default=None)                # Get a Variable object or default
self.system.variables.set(name, value)                       # Update a variable's value
```

Variable names are case-insensitive (stored uppercase internally). Reserved variables cannot be removed.

## Settings & Paths

The `Settings` object (accessible via `self.settings`) contains:

- **`user`** (`User`): user profile — email, username, personal paths
- **`syspaths`** (`SysPaths`): system-wide paths managed by Flux

### SysPaths (key directories)

| Path | Location |
|------|----------|
| `CONFIG_FOLDER` | `~/.flux/` |
| `SETTINGS_FILE` | `~/.flux/settings.json` |
| `SERVICES_FILE` | `~/.flux/services.json` |
| `CACHE_FOLDER` | `~/.flux/cache/` |
| `FLUX_TEMP_FOLDER` | `/tmp/flux-temp/` |
| `LOGS_FOLDER` | `/tmp/flux-temp/logs/` |
| `PIPES_FOLDER` | `/tmp/flux-temp/pipes/` |
| `CMD_BUILTIN_FOLDER` | `flux/core/cmd/builtin/` |
| `CMD_SCRIPTS_FOLDER` | `flux/core/cmd/scripts/` |
| `CMD_FPM_FOLDER` | `flux/core/cmd/fpm/` |
