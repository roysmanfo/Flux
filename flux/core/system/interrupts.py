import sys
import signal
import random
import time
from typing import Any, List, Mapping, Set, Callable, Optional, Tuple, Union
from signal import Signals
from enum import IntEnum


class UnsupportedSignalError(ValueError):
    """
    Error with the provided Event/Signal 
    """


class EventTriggers(IntEnum):
    """
    These are all event the triggers
    """
    SIGABRT = Signals.SIGABRT.value
    SIGFPE = Signals.SIGFPE.value
    SIGILL = Signals.SIGILL.value
    SIGINT = Signals.SIGINT.value
    SIGSEGV = Signals.SIGSEGV.value
    SIGTERM = Signals.SIGTERM.value

    if sys.platform == "win32":
        SIGBREAK = Signals.SIGBREAK.value
        CTRL_C_EVENT = Signals.CTRL_C_EVENT.value
        CTRL_BREAK_EVENT = Signals.CTRL_BREAK_EVENT.value
    else:
        SIGALRM = Signals.SIGALRM.value
        SIGBUS = Signals.SIGBUS.value
        SIGCHLD = Signals.SIGCHLD.value
        SIGCONT = Signals.SIGCONT.value
        SIGHUP = Signals.SIGHUP.value
        SIGIO = Signals.SIGIO.value
        SIGIOT = Signals.SIGIOT.value
        SIGKILL = Signals.SIGKILL.value
        SIGPIPE = Signals.SIGPIPE.value
        SIGPROF = Signals.SIGPROF.value
        SIGQUIT = Signals.SIGQUIT.value
        SIGSTOP = Signals.SIGSTOP.value
        SIGSYS = Signals.SIGSYS.value
        SIGTRAP = Signals.SIGTRAP.value
        SIGTSTP = Signals.SIGTSTP.value
        SIGTTIN = Signals.SIGTTIN.value
        SIGTTOU = Signals.SIGTTOU.value
        SIGURG = Signals.SIGURG.value
        SIGUSR1 = Signals.SIGUSR1.value
        SIGUSR2 = Signals.SIGUSR2.value
        SIGVTALRM = Signals.SIGVTALRM.value
        SIGWINCH = Signals.SIGWINCH.value
        SIGXCPU = Signals.SIGXCPU.value
        SIGXFSZ = Signals.SIGXFSZ.value
        if sys.platform != "linux":
            SIGEMT = Signals.SIGEMT.value
            SIGINFO = Signals.SIGINFO.value
        if sys.platform != "darwin":
            SIGCLD = Signals.SIGCLD.value
            SIGPOLL = Signals.SIGPOLL.value
            SIGPWR = Signals.SIGPWR.value
            SIGRTMAX = Signals.SIGRTMAX.value
            SIGRTMIN = Signals.SIGRTMIN.value
            if sys.version_info >= (3, 11):
                SIGSTKFLT = Signals.SIGSTKFLT.value

    # these are exclusive to flux
    PROCESS_CREATED = 100           # Triggered when a new process is created
    PROCESS_DELETED = 101           # Triggered when a new process is deleted
    # available but not yet working
    COMMAND_EXECUTED = 102          # Triggered after a command is successfully executed
    COMMAND_FAILED = 103            # Triggered if a command execution fails
    DIRECTORY_CHANGED = 104         # Triggered when the current working directory is changed
    FILE_MODIFIED = 105             # Triggered when a file is modified within the current directory
    SIGNAL_RECEIVED = 106           # Triggered when a signal is received by the terminal
    TASK_COMPLETED = 107            # Triggered when a long-running task completes
    TASK_FAILED = 108               # Triggered when a long-running task fails
    NETWORK_CONNECTED = 109         # Triggered when a network connection is established
    NETWORK_DISCONNECTED = 110      # Triggered when a network connection is lost
    USER_LOGIN = 111                # Triggered when a user logs into the system
    USER_LOGOUT = 112               # Triggered when a user logs out of the system
    SYSTEM_ERROR = 113              # Triggered when a system error occurs
    MEMORY_USAGE_HIGH = 114         # Triggered when memory usage exceeds a certain threshold
    CPU_USAGE_HIGH = 115            # Triggered when CPU usage exceeds a certain threshold
    BATTERY_LOW = 116               # Triggered when the battery level is low (for portable devices)

def event_name_to_value(event: str) -> Optional[int]:
    try:
        return EventTriggers[event]
    except KeyError:
        return None


def event_value_to_name(value: int) -> Optional[str]:
    if value not in EventTriggers:
        return None

    return _clean_event_name(EventTriggers(value))


def _clean_event_name(event_repr: str) -> str:
    return event_repr.__repr__().removeprefix("<EventTriggers.").split(":")[0].upper()


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
    def __init__(self,
                 handle: IHandle,
                 signal: int,
                 target: Callable[[Any], None],
                 args: Optional[Tuple[Any]] = (),
                 kwargs: Optional[Mapping[str, Any]] = None,
                 exec_once: Optional[bool] = None
                ) -> None:
        self.HANDLE = handle
        self.signal = signal
        self.target = target
        self.args = args
        self.kwargs = kwargs if kwargs is not None else dict()
        self.exec_once = exec_once if exec_once is not None else True
        self.exec_count = 0

    @property
    def handle(self):
        """
        alias for self.HANDLE
        """
        return self.HANDLE

    @property
    def executed(self):
        return self.exec_count > 0

    @property
    def is_dead(self):
        return self.executed and self.exec_once

    def call(self, signum, frame) -> None:
        """
        Execute the code in the interrupt function
        """

        if self.target:
            self.target(signum, frame, *self.args, *self.kwargs)
            self.exec_count += 1


class InterruptHandler(object):
    def __init__(self) -> None:
        self.interrupts: dict[int, list[Interrupt]] = {}
        self.interrupt_map: dict[IHandle, Interrupt] = {}
        self.supported: dict[str, int] = {}

        # add all available interrupts to self
        for event in list(EventTriggers):
            try:
                if event in Signals:
                    signal.signal(event, self._handle_interrupts)

                event_name = event_value_to_name(event)
                self.supported.update({event_name: int(event)})
            except ValueError:
                pass

    def register(self,
                 event: Union[Signals, EventTriggers],
                 target: Callable[[Any], None],
                 args: Optional[Tuple[Any]] = (),
                 kwargs: Optional[Mapping[str, Any]] = None,
                 exec_once: Optional[bool] = True
                ) -> IHandle:
        """
        Register a new interrupt handler

        `:param` event: can be one of the supported `Signals` or `EventTriggers`. Specifies when to execute the interrupt
        `:param` target: the actual code to execute once the specified event occours  
        `:param` args: the arguments needed by the target function   
        `:param` kwargs: is a dictionary of keyword arguments for the target invocation. Defaults to {}.   
        `:param` exec_once: if set to False, the interrupt will be executed at each event, as long as the command is still alive
        `:returns` an handle to the `Interrupt`, which will be useful when interacting with it
        """

        if not isinstance(event, (Signals, EventTriggers)):
            raise UnsupportedSignalError("You must provide a Signal/Event")

        signal_value = event.value if isinstance(event, EventTriggers) else event

        if signal_value not in EventTriggers or signal_value not in Signals:
            raise UnsupportedSignalError(
                "The specified EventTriggers isn't suported")

        h = IHandle.generate_handle()

        # avoid shared handles
        while h in self.interrupt_map:
            h = IHandle.generate_handle()

        handle = IHandle(h)
        if type(args) != tuple:
            args = (args,)
        if kwargs and type(kwargs) != dict:
            raise TypeError(f"kwargs should be of type dict and not {type(kwargs)}")
        interrupt = Interrupt(handle, signal_value, target, args, kwargs, exec_once)

        if signal_value not in self.interrupts:
            self.interrupts[signal_value] = []
        self.interrupts[signal_value].append(interrupt)

        self.interrupt_map[handle] = interrupt
        return handle

    def unregister(self, handle: IHandle, force: bool = False) -> bool:
        """
        Unregister an interrupt handler

        `:param` handle: an handle to the Interrupt to remove
        `:param` force: if True, the interrupt will be removed even if it hasn't been executed yet
        `:returns` True if the interrupt has been removed, or has not been found, False otherwise
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

    def get_supported_signals(self) -> Set[str]:
        return set(self.supported.keys())

    def _handle_interrupts(self, signum, frame) -> None:
        # Call all appropriate interrupts based on the interrupt type
        if signum and signum in self.interrupts:
            for interrupt in self.interrupts[signum]:
                interrupt.call(signum, frame)

    def get_all(self, event: Union[Signals, EventTriggers]) -> List[Interrupt]:
        """
        `:returns` a list of all interupts with a specific trigger event
        """
        return self.interrupts.get(event, [])

    def get(self, event: Union[Signals, EventTriggers]) -> Optional[Interrupt]:
        """
        `:returns` the first interrupt with a specific trigger event, None if not found
        """
        vals = self.get_all(event)
        return vals[0] if vals else None

    def find(self, handle: IHandle) -> Optional[Interrupt]:
        """
        `:returns` the first interrupt with a specific handle using a linear search, None if not found
        """
        return self.interrupt_map.get(handle, None)

    def get_available_signals(self) -> dict:
        return self.supported

    def get_available_signals_names(self) -> List[str]:
        return list(self.supported.keys())

    def get_available_signal_values(self) -> List[int]:
        return list(self.supported.values())
