from abc import ABCMeta as _ABCMeta, abstractmethod as _abstractmethod
import os
from typing import Callable, Optional

from flux.core.system.system import System


def service_info_manager(func: Callable[[], None]):
    is_running = func.__name__ == "start"

    def wrapper(self, *args, **kwargs):
        self._running = is_running
        return func(self, *args, **kwargs)
    
    return wrapper


class ServiceInterface(metaclass=_ABCMeta):
    """
    A service is a background program that is allowed to run as soon as the
    program starts 
    
    """

    def __init__(self,
                 system: System,
                 name: Optional[str] = None,
                ) -> None:

        self.system: System = system
        self._name: str = name or os.path.splitext(os.path.basename(__file__))[0]
        
        # informations about the service
        self.metadata = {
            "name": self._name,
            "description":"",
        }

        self._running: bool = False
        self._enabled: bool = False


    def __init_subclass__(cls) -> None:
        cls._FLUX_SERVICE = True

    @staticmethod
    def _is_subclass(cls) -> bool:
        self_mro = [i.__name__ for i in ServiceInterface.mro()]
        cls_mro = [i.__name__ for i in cls.mro()[-len(self_mro):]]
        return cls_mro == self_mro

    @staticmethod
    def _is_subclass_instance(instance: object) -> bool:
        _FLUX_SERVICE = getattr(instance, "_FLUX_SERVICE", None)
        return _FLUX_SERVICE and isinstance(_FLUX_SERVICE, bool)

    @service_info_manager
    def start(self) -> None:
        """
        Start the service by calling `update()` 
        """
        try:
            self.awake()
            while self.running:
                self.update()
        except Exception:
            pass
        self.stop()
        
    
    def awake(self) -> None:
        """
        Called once as soon as the service gets started
        """
        ... 

    @_abstractmethod
    def update(self) -> None:
        """
        Operations to perform when the current service gets started
        """
        ... 

    @service_info_manager
    def stop(self):
        """
        Operations to perform when the current service gets stopped 
        """
        self._running = False

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

