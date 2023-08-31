from threading import Thread
import time
from typing import List, Callable
import os

# Process status codes
STATUS_OK = 0
STATUS_ERR = 1


class Process:
    def __init__(self, id: int, owner: str, command_instance: Callable, line_args: list[str]) -> None:
        self.id: int = id
        self.name: str = line_args[0]
        self.owner: str = owner
        self.command_instance: Callable = command_instance
        self.line_args: List[str] = line_args
        self.started: float = time.time()
        self.status: int | None = None
        self.thread: Thread = None

    def _calculate_time(self, seconds: float) -> str:
        minutes = int(seconds / 60)
        hours = int(minutes / 60)
        seconds = int(seconds % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"

        if minutes > 0:
            return f"{minutes}m {seconds}s"

        return f"{seconds}s"

    def run(self, is_main_thread = False):
        if is_main_thread:
            self.thread = Thread(target=self.command_instance, name=self.line_args[0])
            self.thread.start()
            return
        
        self.thread = Thread(target=self._run, name=self.line_args[0], daemon=True)
        self.thread.start()

    def _run_main(self):
        self.command_instance()

    def _run(self):
        self.command_instance.init()
        self.command_instance.run(self.line_args)
        self.command_instance.close()
        self.status = self.command_instance.exit()

    def __str__(self) -> str:
        return f"{self.id}\t{self.owner}\t{self.thread.name}\t{self._calculate_time(self.started - time.time())}"

    def all_info(self) -> str:
        return f"{self.id}\t{self.owner}\t{self.thread.name}\t{self.thread.native_id}\t{self._calculate_time(self.started - time.time())}"


class Processes:
    def __init__(self):
        self.processes: list[Process] = []
        self.process_counter: int = os.getpid()

    def list(self) -> list[Process]:
        # Avoid returning the system managed list of processes
        # Instead return a copy
        return self.processes.copy()
    
    def _generate_pid(self) -> int:
        self.process_counter += 1
        return self.process_counter

    def _add_main_process(self, info: object, prog_name: str, callable: Callable):
        self.processes.append(Process(id=self._generate_pid(),owner=info.user.username, command_instance=callable, line_args=prog_name))
        self.processes[-1].run(is_main_thread=True)

    def add(self, info: object, line_args: List[str], callable: Callable):
        self.processes.append(Process(id=self._generate_pid(),owner=info.user.username, command_instance=callable, line_args=line_args))
        print(f"[{self.processes[-1].id}] {line_args[0]}")
        self.processes[-1].run()
        time.sleep(.1)

    def find(self, id: int) -> Process | None:
        for p in self.processes:
            if p.id == id:
                return p
        return None

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
