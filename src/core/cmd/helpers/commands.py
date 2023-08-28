from src.settings.info import Info
import sys
from typing import TextIO

STATUS_OK = 0
STATUS_ERR = 1


class CommandInterface:
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.
    
    ### GENERAL ATTRIBUTES
    Attributes shared by commands

    - `IS_THREAD (const, bool)`     Whether or not the command is being runned as a thread 
    - `info (variable, Info)`       A reference to the instance of the Info class, containing process information 
    - `stdout (variable, TextIO)`   The stdout of the command
    - `stderr (variable, TextIO)`   The stderr of the command
    - `stdin (variable, TextIO)`    The stdin of the command

    ### AUTOMATIC FUNCTIONS
    Functions that get called regardless by the terminal

    - `init()`      This is function is called right before run().
    - `run()`       This is the entry function for the command.
    - `close()`     This is the function that gets called right after run() the command. 
    - `exit()`      This is the last function that gets called.

    """


    def __init__(self,
                 info: Info,
                 is_thread: bool,
                 stdout: TextIO = sys.stdout, 
                 stderr: TextIO = sys.stdout, 
                 stdin: TextIO = sys.stdout
                ) -> None:
        
        self.IS_THREAD: bool = is_thread
        self.info: Info = info
        self.status: int | None = None
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin

    """
    AUTOMATIC CALLS
    """

    def init(self, *args, **kwargs):
        """
        This is function is called right before run().\n
        This function should be used to do setup operations
        """
        ...
    
    def run(self, command: list[str], *args, **kwargs):
        """
        This is the entry function for the command.\n
        This function should be used to manage arguments and adapt command execution.
        """
        ...

    def close(self):
        """
        This is the function that gets called after we run the command.\n
        This function should be used to handle cases like the command being executed as a background task,
        or to do some cleaning after the command executed.
        """
        ...

    def exit(self):
        """
        This is the last function that gets called.\n
        This function should be used to definetly close execution.
        """
        return self.status if self.status else STATUS_OK

    """
    HELPER FUNCTIONS
    """

    def error(self, status: int | None = None, msg: str | None = None):
        """
        This function should be called once an error accoures errors.\n
        This function should be called to handle errors.
        """
        self.stderr.write(f"{self.parser.prog}: {msg}\n\n")
        self.status = status
