from threading import Thread
import time as _time
from typing import List, Callable, Optional, Union
import os as _os
from enum import IntEnum

from flux.core.system.interrupts import EventTriggers, InterruptHandler


class Status(IntEnum):
    STATUS_OK = 0  # Exited with no problems
    STATUS_ERR = 1  # An error accoured
    STATUS_WARN = 2  # Exited with warnings

class ProcessInfo:
    def __init__(self, id: int, ppid: int, owner: str, name: str, native_id: int, time_alive: str, is_reserved_process: bool, line_args: List[str]) -> None:
        self.id = id
        self.ppid = ppid
        self.owner = owner
        self.name = name
        self.native_id = native_id
        self.time_alive = time_alive
        self.is_reserved_process = is_reserved_process
        self.line_args = line_args

    def __str__(self) -> str:
        s = "ProcessInfo("
        s += f"id={self.id}, "
        s += f"ppid={self.ppid}, "
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
        self.started_time: float = _time.time()
        self.status: Optional[int] = None
        self.thread: Thread = None
        self.native_id: Optional[int] = None
        self.is_reserved_process = is_reserved_process


        if command_instance and hasattr(command_instance, "parser") and hasattr(command_instance.parser, "prog"):
            self.name = command_instance.parser.prog or self.name

    def get_info(self) -> ProcessInfo:
        return ProcessInfo(self.id,
                           _os.getppid(),
                           self.owner,
                           self.name,
                           self.native_id,
                           self._calculate_time(_time.time() - self.started_time),
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
            self.native_id = _os.getpid()
            self.thread()
            return

        self.thread = Thread(target=self._run, name=self.name, daemon=True)
        self.thread.start()
        self.native_id = self.thread.native_id

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


_main_process: Process

class Processes:
    def __init__(self, i_handler: InterruptHandler):
        self.processes: dict[int, Process] = {}
        self.process_counter: int = _os.getpid()
        self.i_handler = i_handler

    def list(self) -> List[ProcessInfo]:
        return [p.get_info() for p in self.processes.values()]

    def _generate_pid(self) -> int:
        self.process_counter += 1
        return self.process_counter

    def _add_main_process(self, system: object, prog_name: List[str], callable: Callable):
        global _main_process

        pid = self._generate_pid()
        p = Process(id=pid, owner=system.settings.user.username,
                    command_instance=callable, line_args=prog_name, is_reserved_process=True)
        _main_process = p
        self.processes.update({pid: p})
        self.processes[pid].run(is_main_thread=True)

    def add(self, system: object, line_args: List[str], command_instance: object, is_reserved: bool):
        pid = self._generate_pid()
        self.processes.update({pid: Process(id=pid, owner=system.settings.user.username,
                              command_instance=command_instance, line_args=line_args, is_reserved_process=is_reserved)})
        print(f"[{pid}] {line_args[0]}")
        self.i_handler.raise_interrupt(EventTriggers.PROCESS_CREATED)
        self.processes[pid].run()
        _time.sleep(.1)

    def find(self, id: int) -> Optional[Process]:
        return self.processes.get(id)

    def select(self,
               *,
               id: Optional[int] = None,
               name: Optional[str] = None,
               owner: Optional[str] = None,
               reserved: Optional[bool] = None,
               ) -> List[Process]:
        """
        Search a group of processes that match the rule

        `:param` id: the pid of the process to search (if you have this, results are faster with the `find()` method)
        `:param` name: the name of the process to search
        `:param` owner: the owner of the process
        `:param` reserved: get only reserved processes
        """

        def _filter(p: Process) -> bool:
            if id and p.id != id:
                return False
            if name and p.name != name:
                return False
            if owner and p.owner != owner:
                return False
            if reserved and not p.is_reserved_process:
                return False
            return True

        return list(filter(_filter, self.processes.values()))


    def remove(self, id: int) -> Optional[Process]:
        """
        Returns the removed process if found, None otherwise
        """
        try:
            if id == _main_process.id:
                return None

            proc = self.processes.pop(id)
            self.i_handler.raise_interrupt(EventTriggers.PROCESS_DELETED)
            return proc
        except KeyError:
            return None

    def clean(self) -> None:
        """
        Removes all stoped processes.

        This function is automaticaly called each time the manager handles a command
        """
        status_dict: dict[Status, bool] = {
            Status.STATUS_ERR: False,
            Status.STATUS_OK: False,
            Status.STATUS_WARN: False,
        }
        completed_processes = []
        for p in self.processes.values():
            # check that we are not trying to remove the main process
            if not p is _main_process and not p.thread.is_alive():
                # do not modify the dictionary inside the loop
                # but still keep track of all the processes to remove
                completed_processes.append(p.id)
                try:
                    # p.staus should have a value assigned, but check (just in case)
                    if isinstance(p.status, Status):
                        status_dict[p.status] = True
                except:
                    # a non valid status was received (probably some other data type),
                    # ignore it as we don't know what does it mean
                    pass

        for pid in completed_processes:
            self.processes.pop(pid)

        self.i_handler.raise_interrupt(EventTriggers.PROCESS_DELETED)

        if status_dict[Status.STATUS_ERR]:
            self.i_handler.raise_interrupt(EventTriggers.COMMAND_FAILED)
        elif status_dict[Status.STATUS_OK] or status_dict[Status.STATUS_WARN]:
            self.i_handler.raise_interrupt(EventTriggers.COMMAND_FAILED)

    def copy(self):
        processes = Processes(i_handler=self.i_handler)
        processes.processes = self.processes.copy()
        return processes
