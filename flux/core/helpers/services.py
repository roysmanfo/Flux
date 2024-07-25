from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Callable

from flux.core.system.system import System


def service_info_manager(func: Callable[[], None]):
    def wrapper(self, *args, **kwargs):
        self._running = True
        return func(*args, **kwargs)
    
    return wrapper


class ServiceInterface(_ABC):
    """
    A service is a background program that is allowed to run as soon as the
    program starts 
    
    """

    def __init__(self,
                 system: System,
                ) -> None:

        self._running: bool = False
        self._enabled: bool = False
        self.system: System = system

    @_abstractmethod
    @service_info_manager
    def start(self) -> None:
        """
        Operations to perform when the current service gets started 
        """
        ... 

    @_abstractmethod
    @service_info_manager
    def stop(self):
        """
        Operations to perform when the current service gets stopped 
        """
        ...

    @property
    def running(self) -> bool:
        return self._running

    @property
    def enabled(self) -> bool:
        """
        if true, then this means that the service is allowed to run automatically
        as soon as the terminal is spawned  
        """
        return self._enabled

