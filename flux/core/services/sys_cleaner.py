from flux.core.interfaces import ServiceInterface


class Service(ServiceInterface):
    def awake(self):
        # run every 3s
        self.cooldown = 3

        self.metadata["description"] = (
            "Periodically run system cleanups to remove things like dead processes"
        )

    def update(self):
        self.system.processes.clean()
