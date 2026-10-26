from flux.core.interfaces.services import ServiceInterface


class Service(ServiceInterface):

    def awake(self):

        self.metadata = {
            "name": self._name,
            "description": "print interrupt signals when they are detected (for debug)",
        }



        # making a service register an interrupt is bad practice as there is not yet a way to safely
        # determine when and how to remove it (we are makign an exeption here, as this service should not be stopped)
        for e in self.system.interrupt_handler.supported.values():
            self.system.interrupt_handler._register(e, self.capture, exec_once=False)
    
    def update(self):
        pass

    def capture(self, signum, frame):
        # debug
        print(signum)

        


