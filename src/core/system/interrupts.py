from typing import Any, Callable, Optional, Union
from signal import Signals
from enum import IntEnum, auto
import random
import time


class UnsupportedSignalError(ValueError):
    """
    Error with the provided Event/Signal 
    """


class Events(IntEnum):
    """
    These interupt values are specific references to internal flux processes 
    """
    PROCESS_CREATED: int = auto()           # Triggered when a new process is created
    PROCESS_DELETED: int = auto()           # Triggered when a new process is deleted
    # available but not yet working
    COMMAND_EXECUTED: int = auto()          # Triggered after a command is successfully executed
    COMMAND_FAILED: int = auto()            # Triggered if a command execution fails
    DIRECTORY_CHANGED: int = auto()         # Triggered when the current working directory is changed
    FILE_MODIFIED: int = auto()             # Triggered when a file is modified within the current directory
    SIGNAL_RECEIVED: int = auto()           # Triggered when a signal is received by the terminal
    TASK_COMPLETED: int = auto()            # Triggered when a long-running task completes
    TASK_FAILED: int = auto()               # Triggered when a long-running task fails
    NETWORK_CONNECTED: int = auto()         # Triggered when a network connection is established
    NETWORK_DISCONNECTED: int = auto()      # Triggered when a network connection is lost
    USER_LOGIN: int = auto()                # Triggered when a user logs into the system
    USER_LOGOUT: int = auto()               # Triggered when a user logs out of the system
    SYSTEM_ERROR: int = auto()              # Triggered when a system error occurs
    MEMORY_USAGE_HIGH: int = auto()         # Triggered when memory usage exceeds a certain threshold
    CPU_USAGE_HIGH: int = auto()            # Triggered when CPU usage exceeds a certain threshold
    BATTERY_LOW: int = auto()               # Triggered when the battery level is low (for portable devices)


class IHandle(int):
    """
    Interrupt Handle

    This allows to identify and interact with a specific interrupt
    """
    
    def __str__(self) -> str:
        return f"IHandle<{super().__str__()}>"

    @staticmethod
    def generate_handle():
        return int(time.time()) // random.randint(1000, 9999)


class Interrupt:
    def __init__(self, handle: IHandle, signal: int, callback: Callable[[Any], None], exec_once: Optional[bool] = None) -> None:
        self.HANDLE = handle
        self.signal = signal
        self.callback = callback
        self.exec_once = exec_once if exec_once is not None else True
        self.exec_count = 0

    @property
    def handle(self):
        return self.HANDLE
    
    @property
    def executed(self):
        return self.exec_count > 0
    
    @property
    def is_dead(self):
        return self.executed and self.exec_once 
    
    def call(self) -> None:
        """
        Execute the code in the interrupt function
        """
        
        if self.callback:
            self.callback()
            self.exec_count += 1

        

class InterruptHandler(object):
    def __init__(self) -> None:
        self.interrupts: dict[int, list[Interrupt]] = {}
        self.interrupt_map: dict[IHandle, Interrupt] = {}
        self.supported: dict[str, int] = {}

    def register(self, signal: Union[Signals, Events], callback: Callable[[Any], None], exec_once: Optional[bool] = True) -> IHandle:
        """
        Register a new interrupt handler

        `:param signal` can be one of the supported `Signals` or `Events`. Specifies when to execute the interrupt
        `:param callback` the actual code to execute once the specified event accours  
        `:param exec_once` if set to False, the interrupt will be executed at each event, as long as the command is stil alive
        `:returns` an handle to the `Interrupt`, which will be usefull when interacting with it
        """

        if not isinstance(signal, (Signals, Events)):
            raise UnsupportedSignalError("You must provide a Signal/Event")
        
        signal_value = signal.value if isinstance(signal, Events) else signal
        
        if signal_value not in Events or signal_value not in Signals:
            raise UnsupportedSignalError("The specified Event/Signal isn't suported")

        h = IHandle.generate_handle()

        # avoid shared handles
        while h in self.interrupt_map:
            h = IHandle.generate_handle()

        handle = IHandle(h)
        
        interrupt = Interrupt(handle, signal_value, callback, exec_once)
        
        if signal_value not in self.interrupts:
            self.interrupts[signal_value] = []
        self.interrupts[signal_value].append(interrupt)

        self.interrupt_map[handle] = interrupt
        return handle


    def unregister(self, handle: IHandle, force: bool = False) -> bool:
        """
        Unregister an interrupt handler

        `:param handle` an handle to the Interrupt to remove
        `:param force` if True, the interrupt will be removed even if it hasn't been executed yet
        `:returns` True if the interrupt hase been removed, or has not been found, False otherwise
        """

        interrupt = self.interrupt_map.get(handle)
        if not interrupt:
            return True
        
        if interrupt.executed or force:
            # remove from mapping
            self.interrupt_map.pop(handle)

            # remove from database
            self.interrupts.get(interrupt.signal).remove(interrupt)

            # delete from memory
            del interrupt

            return True
        return False
    
    def _handle_interrupts(self, signum: int, frame: object) -> None:
        print(f"Signal {signum} received")

        # Call all appropriate interrupts based on the interrupt type
        if signum in self.interrupts:
            for interrupt in self.interrupts[signum]:
                interrupt.call()

    def get_all(self, sig_type: Union[Signals, Events]) -> list[Interrupt]:
        """
        `:returns`
        a list of all interupts with a specific type of interrupt using a linear search
        """
        return [i for i in self.interrupts if i.signal == sig_type]
    
    def get(self, sig_type: Union[Signals, Events]) -> Interrupt | None:
        """
        `:returns`
        the first interrupt with a specific type of interrupt using a linear search, None if not found
        """
        for i in self.interrupts.values():
            for j in i:
                if j.signal == sig_type:
                    return i 
        return None
    
    def find(self, handle: IHandle) -> Interrupt | None:
        """
        `:returns`
        the first interrupt with a specific handle using a linear search, None if not found
        """
        return self.interrupt_map.get(handle, None)

    def get_available_signals(self) -> dict:
        return self.supported

    def get_available_signals_names(self) -> list[str]:
        return list(self.supported.keys())

    def get_available_signal_values(self) -> list[int]:
        return list(self.supported.values())

