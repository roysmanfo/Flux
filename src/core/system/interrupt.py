from typing import Any, Callable
from signal import Signals

class Interrupt:
    def __init__(self, signal: Signals, callback: Callable[[Any], None]) -> None:
        self.signal = signal
        self.callback = callback


    def call(self) -> None:
        """
        Execute the code in the interrupt function
        """
        if self.callback:
            self.callback()

class InterruptHandler(object):
    def __init__(self) -> None:
        self.interrupts: list[Interrupt] = []

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

    def handle_interrupts(self, signum, frame) -> None:
        print(signum) # check if everything works

        # TODO: call all appropriate interrupts based on the interrupt type 

