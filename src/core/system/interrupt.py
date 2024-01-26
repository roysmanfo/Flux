from typing import Any, Callable, Optional
from signal import Signals

class Interrupt:
    def __init__(self, signal: int, callback: Callable[[Any], None], exec_once: Optional[bool] = None) -> None:
        self.signal = signal
        self.callback = callback
        self.exec_once = exec_once


    def call(self) -> None:
        """
        Execute the code in the interrupt function
        """
        if self.callback:
            self.callback()

class InterruptHandler(object):
    def __init__(self) -> None:
        self.interrupts: list[Interrupt] = []
        self.supported: dict[str, int] = {}

    def search_all(self, sig_type: Signals) -> list[Interrupt]:
        """
        `:returns`
        a list of all interupts with a specific type of interrupt using a linear search
        """
        return [i for i in self.interrupts if i.signal == sig_type]
    
    def search(self, sig_type: Signals) -> Interrupt | None:
        """
        `:returns`
        the first interrupt with a specific type of interrupt using a linear search, None if not found
        """
        for i in self.interrupts:
            if i.signal == sig_type:
                return i 
        return None

    def get_available_signals(self) -> dict:
        return self.supported

    def get_available_signals_names(self) -> list[str]:
        return list(self.supported.keys())

    def get_available_signal_values(self) -> list[int]:
        return list(self.supported.values())

    def _handle_interrupts(self, signum, frame) -> None:
        print(signum) # check if everything works

        # TODO: call all appropriate interrupts based on the interrupt type 

