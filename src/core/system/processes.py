from threading import Thread
import time


# Process status codes
STATUS_OK = 0
STATUS_ERR = 1


class Process:
    def __init__(self, id: int, owner: str, thread: Thread) -> None:
        self.id = id
        self.owner = owner
        self.thread = thread
        self.started = time.time()

    def _calculate_time(self, seconds: float) -> str:
        minutes = int(seconds / 60)
        hours = int(minutes / 60)
        seconds = int(seconds % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"

        if minutes > 0:
            return f"{minutes}m {seconds}s"

        return f"{seconds}s"

    def __str__(self) -> str:
        return f"{self.id}\t{self.owner}\t{self.thread.name}\t{self._calculate_time(self.started - time.time())}"

    def all_info(self) -> str:
        return f"{self.id}\t{self.owner}\t{self.thread.name}\t{self._calculate_time(self.started - time.time())}"


class Processes:
    def __init__(self):
        self.processes: list[Process] = []

    def list(self, show_all: bool = False):
        """
        If all is true, all process info is shown 
        """
        for p in self.processes:
            if p.thread.native_id is not None and not show_all:
                print(p)
            else:
                print(p.all_info())

    def add(self, info: object, thread: Thread):
        self.processes.append(
            Process(id=thread.native_id, owner=info.user.username, thread=thread))
        self.processes[-1].thread.start()

    def remove(self, id) -> Process:
        for p in self.processes:
            if p.id == id:
                self.processes.remove(p)
                return p
        return None

    def clean(self) -> None:
        """
        Removes all stoped processes.

        This function is automaticaly called each time the manager handles a command
        """

        for p in self.processes:
            if not p.thread.is_alive():
                self.processes.remove(p)
