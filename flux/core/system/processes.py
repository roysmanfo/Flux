from threading import Thread
import time as _time
from typing import List, Callable, Optional, Union
import os as _os
from enum import IntEnum


class Status(IntEnum):
    STATUS_OK = 0  # Exited with no problems
    STATUS_ERR = 1  # An error accoured
    STATUS_WARN = 2  # Exited with warnings


class ProcessInfo:
    def __init__(self, id: int, pid: int, owner: str, name: str, native_id: int, time_alive: str, is_reserved_process: bool, line_args: List[str]) -> None:
        self.id = id
        self.pid = pid
        self.owner = owner
        self.name = name
        self.native_id = native_id
        self.time_alive = time_alive
        self.is_reserved_process = is_reserved_process
        self.line_args = line_args

    def __str__(self) -> str:
        s = "ProcessInfo("
        s += f"id={self.id}, "
        s += f"pid={self.pid}, "
        s += f"owner={self.owner}, "
        s += f"name={self.name}, "
        s += f"native_id={self.native_id}, "
        s += f"is_reserved_process={self.is_reserved_process}, "
        s += f"time_alive={self.time_alive}"
        s += f"line_args={self.line_args}"
        s += ")"
        return s

    def __repr__(self) -> str:
        return self.__str__()


class Process:
    def __init__(self, id: int, owner: str, command_instance: Union[Callable, object], line_args: List[str], is_reserved_process: bool) -> None:
        self.id: int = id
        self.name: str = line_args[0]
        self.owner: str = owner
        self.command_instance: Callable = command_instance
        self.line_args: List[str] = line_args
        self.started: float = _time.time()
        self.status: Optional[int] = None
        self.thread: Thread = None
        self.native_id: Optional[int] = None
        self.is_reserved_process = is_reserved_process

    def get_info(self) -> ProcessInfo:
        return ProcessInfo(self.id,
                           _os.getppid(),
                           self.owner,
                           self.name,
                           self.native_id,
                           self._calculate_time(_time.time() - self.started),
                           self.is_reserved_process,
                           self.line_args
                           )

    def __str__(self) -> str:
        return self.get_info().__str__()

    def _calculate_time(self, seconds: float) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        
        if minutes > 0:
            return f"{int(minutes)}m {int(seconds)}s"

        return f"{int(seconds)}s"


    def run(self, is_main_thread=False):
        if is_main_thread:
            self.thread = self._run_main
            self.thread()
            self.native_id = _os.getpid()
            return

        self.thread = Thread(target=self._run, name=self.name, daemon=True)
        self.thread.start()

    def _run_main(self):
        self.command_instance()

    def _run(self):
        try:
            self.command_instance.init()
            self.command_instance.setup()

            if self.command_instance.parser and self.command_instance.parser.exit_execution:
                self.command_instance.close()
                self.status = self.command_instance.exit()
                return

            self.command_instance.run()
            self.command_instance.close()
            self.status = self.command_instance.exit()
        
        except Exception as e:
            self.command_instance.fail_safe(e)
            self.status = self.command_instance.status


        print(f"[{self.id}] {self.name} stopped")


class Processes:
    def __init__(self):
        self.processes: List[Process] = []
        self.process_counter: int = _os.getpid()

    def list(self) -> List[ProcessInfo]:
        # Avoid returning the system managed list of processes
        # Instead return a copy
        return [p.get_info() for p in self.processes.copy()]

    def _generate_pid(self) -> int:
        self.process_counter += 1
        return self.process_counter

    def _add_main_process(self, info: object, prog_name: str, callable: Callable):
        self.processes.append(Process(id=self._generate_pid(), owner=info.user.username,
                              command_instance=callable, line_args=prog_name, is_reserved_process=True))
        self.processes[-1].run(is_main_thread=True)

    def add(self, info: object, line_args: List[str], command_instance: object, is_reserved: bool):
        self.processes.append(Process(id=self._generate_pid(), owner=info.user.username,
                              command_instance=command_instance, line_args=line_args, is_reserved_process=is_reserved))
        print(f"[{self.processes[-1].id}] {line_args[0]}")
        self.processes[-1].run()
        _time.sleep(.1)

    def find(self, id: int) -> Union[Process, None]:
        for p in self.processes:
            if p.id == id:
                return p
        return None

    def remove(self, id: int) -> Process:
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
            # check that we are not trying to remove the main process 
            if not p is self.processes[0] and not p.thread.is_alive():
                self.processes.remove(p)

    def copy(self):
        processes = Processes()
        processes.processes = self.processes.copy()
        return processes
        
