from src.settings.info import Info

class CommandInterface:
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.
    
    ### GENERAL ATTRIBUTES
    Attributes shared by commands

    - `IS_THREAD (const, bool)`     Whether or not the command is being runned as a thread 
    - `info (variable, Info)`       A reference to the instance of the Info class, containing process information 

    ### AUTOMATIC FUNCTIONS
    Functions that get called regardless by the terminal

    - `init()`      This is function is called right before run().
    - `run()`       This is the entry function for the command.
    - `close()`     This is the function that gets called right after run() the command. 
    - `exit()`      This is the last function that gets called.

    """


    def __init__(self, info: Info, is_thread: bool) -> None:
        self.IS_THREAD = is_thread
        self.info = info

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
        ...

    """
    HELPER FUNCTIONS
    """

    def error(self):
        """
        This function should be called once an error accoures errors.\n
        This function should be called to handle errors.
        """
        ...
