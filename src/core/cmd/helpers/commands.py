

class CommandInterface:
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.
    
    ### FUNCTIONS

    - `init()` This is function is called right before run().   
    - `run()`  This is the entry function for the command.   

    """

    def init(self, *args, **kwargs):
        """
        This is function is called right before run().\n
        This function should be used to do setup operations
        """
        ...
    
    def run(self, command: list[str], info: object, *args, **kwargs):
        """
        This is the entry function for the command.\n
        This function should be used to manage arguments and adapt command execution.
        """
        ...