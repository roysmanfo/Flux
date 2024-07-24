from abc import ABC as _ABC, abstractmethod as _abstractmethod

class Service(_ABC):
    """
    A service is a background program that is allowed to run as soon as the
    program starts 
    
    """
    
    @_abstractmethod
    def start(self):
        pass 

    @_abstractmethod
    def stop(self):
        pass 



