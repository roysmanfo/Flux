

class CommandInterface:
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.
    
    ### FUNCTIONS

    - `init()` This is function is called right before run(). This function should be used to do setup operations   
    - `run()`  This is the entry function for the command. This function should be used to manage arguments   

    """

    def init(self, *args, **kwargs):
        ...
    
    def run(self, command: list[str], info: object, *args, **kwargs):
        ...