import socket
import random

from flux.core.interfaces.services import ServiceInterface
from flux.core.system.interrupts import EventTriggers

class Service(ServiceInterface):

    def awake(self) -> None:
        self.metadata["description"] =  "check every 5 seconds if the internet connection is up"
        self.cooldown: int = 5 # check every 5 seconds

        self.remote_servers = ["1.1.1.1", "www.google.com", "www.facebook.com", "www.twitter.com"]

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)

        # flags
        self.net_connected = False

    def update(self):
        res = self.socket.connect_ex((random.choice(self.remote_servers), 80))
        self.socket.close()

        if res == 0 and not self.net_connected:
            self.system.interrupt_handler.raise_interrupt(EventTriggers.NETWORK_CONNECTED)
            self.net_connected = True

        elif self.net_connected:
            self.net_connected = False
            self.system.interrupt_handler.raise_interrupt(EventTriggers.NETWORK_DISCONNECTED)

    def stop(self):
        try:
            # close the socket if it's still open 
            self.socket.close()
        except:
            pass
    
