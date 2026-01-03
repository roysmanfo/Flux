from abc import abstractmethod as _abstractmethod
import os
import time
from typing import Callable, Optional, final

from flux.core.system.system import System
from flux.utils.security import NoOverrideMeta, prevent_override

def service_info_manager(func: Callable[[], None]):
    is_running = func.__name__ == "start"

    def wrapper(self, *args, **kwargs):
        self._running = is_running
        return func(self, *args, **kwargs)
    
    return wrapper


class ServiceInterface(metaclass=NoOverrideMeta):
    """
    A service is a background program that is allowed to run as soon as the
    program starts

    ### GENERAL ATTRIBUTES
    Helpful data and context for the service

    - `system (variable, System)`               A reference to the instance of the System class, containing all the most important informations about flux
    - `metadata (variable, dict[str, str])`     A dictionary containing the keys 'name' and 'description' of the service
    - `cooldown (variable, float)`              Time in seconds to wait before executing `update()` again
    - `skip_cooldown (variable, bool)`          When set to True, the cooldown will be ignored (may cause a slow down of the rest of Flux)
    
    ### MAIN METHODS
    Methods that get called regardless by the terminal and
    are the core of the service execution
    
    - `start()`             Activates the current service by calling `run()` and setting the `running` flag 
    - `stop()`              Stops the current service by unsetting the `running` flag 
    - `awake()`             Gets called once as soon as the service gets started
    - `update()`            Operations to perform when the current service gets started (called repetedly)


    ### PROPERTIES
    Other usefull informations about the state of the service

    - `bool` `running()`     True when the service is running
    - `bool` `enabled()`     True when the service is allowed to run automatically as soon as the terminal is spawned
    """

    def __init__(self,
                 system: System,
                 name: Optional[str] = None,
                ) -> None:

        self.system: System = system
        self._name: str = name or os.path.splitext(os.path.basename(__file__))[0]
        
        # some operations may be very heavy, so we add a pause
        # prevent a slow down the rest of Flux
        self.skip_cooldown = False
        
        # time in seconds to wait before executing `update()` again
        self.cooldown = .1

        # informations about the service
        self.metadata = {
            "name": self._name,
            "description":"",
        }


        # service flags
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
    @final
    @prevent_override
    def start(self) -> None:
        """
        Start the service by calling `update()` 
        """
        try:
            self.awake()
            while self.running:
                self.update()

                # there will be no wait with skip_cooldown set to True
                time.sleep(self.cooldown * (not bool(self.skip_cooldown)))
        except Exception as e:
            try:
                self.on_error(e)
            except Exception:
                # you never know what could happen
                pass
        finally:
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
    
    def on_error(self, e: Exception) -> None:
        """
        Operations to perform when an error occurs
        """
        ...

    @property
    def running(self) -> bool:
        return self._running

    @property
    def name(self) -> bool:
        return self._name

    @property
    def enabled(self) -> bool:
        """
        if true, then this means that the service is allowed to run automatically
        as soon as the terminal is spawned  
        """
        return self._enabled

