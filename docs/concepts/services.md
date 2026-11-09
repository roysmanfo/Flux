# Services

Flux background services are lightweight programs that run continuously alongside the REPL. They monitor system state, perform periodic cleanup, and raise events through the interrupt handler.

## Built-in services

| Service | Description | Cooldown |
|---------|-------------|----------|
| `sys_usage` | Monitors CPU and memory usage; raises `CPU_USAGE_HIGH` / `MEMORY_USAGE_HIGH` triggers when thresholds are exceeded | ~1s |
| `net_monitor` | Checks network connectivity every 5 seconds; raises `NETWORK_CONNECTED` / `NETWORK_DISCONNECTED` | 5s |
| `sys_cleaner` | Periodically cleans up dead processes, old temporary files | 3s |
| `signal_daemon` | Debug service — logs interrupt signals as they arrive (not enabled by default) | configurable |

## Service lifecycle

A service inherits from `ServiceInterface` and follows this cycle:

```
start() → awake() → [update()] ∞ → stop()
                ↑          |
                └── sleep(cooldown) ──┘
```

| Method | When called | Purpose |
|--------|-------------|---------|
| `start()` | Service is enabled and running | Calls `awake()` once, then loops calling `update()` with cooldown pauses |
| `awake()` | Once at startup | Initialization — set metadata, configure cooldowns |
| `update()` | Repeatedly during execution | Core periodic logic |
| `stop()` | Service is stopped | Cleanup and flag reset |
| `on_error(e)` | If `update()` raises an exception | Error handling (must not raise) |

## Service attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `system` | `System` | — | Reference to the System singleton |
| `metadata` | `dict[str, str]` | `{"name": ..., "description": ""}` | Service name and description |
| `cooldown` | `float` | `0.1` | Seconds between `update()` calls |
| `skip_cooldown` | `bool` | `False` | If True, run `update()` without waiting |
| `_running` | `bool` | — | Whether the service is actively running |
| `_enabled` | `bool` | False | Whether the service starts automatically at boot |

## Writing a service

Services live in `flux/core/services/`. Create a Python file and define a `Service` class:

```python
from flux.core.interfaces.services import ServiceInterface

class MyService(ServiceInterface):
    def awake(self) -> None:
        self.metadata["description"] = "My custom background task"
        self.cooldown = 2.0

    def update(self) -> None:
        # This runs every 2 seconds while the service is running
        pass
```

### Enabling/disabling services

Services are managed through `~/.flux/services.json`. Edit this file to toggle which services start automatically when Flux launches. The `service_manager` (accessible via `self.system.service_manager`) handles starting, stopping, and restarting services at runtime.

### Raising events from services

Services can trigger interrupts (event handlers registered by commands) using the system's interrupt handler:

```python
from flux.core.system.interrupts import EventTriggers

def update(self):
    if self._is_high_usage():
        self.system.interrupt_handler.raise_interrupt(EventTriggers.CPU_USAGE_HIGH)
```

## Service discovery

Services are loaded dynamically by `loader.load_service()` using the same LRU-cached mechanism as commands. The loader searches `flux/core/services/` for Python files and instantiates their `Service` (or custom `ENTRY_POINT`) class.
