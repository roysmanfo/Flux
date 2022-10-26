import json, os, platform

class User():
    """
    ### CLASS USER
    The class User manages all user info and settings, plus this
    approach makes working with user properties much easier than in
    the previus version of Cristal, where all settings where also stored
    in a single json file like in this version, but to access it it wes
    neccessary to pass multiple parameters to a function, which will pass
    them to anoather function and make refactoring much harder.

    By using an instance of this class, we need to just pass the current
    user istance (USER) and accessing its settings like with any normal
    python object:
    
    Example: 
    ```py
    send_email(sender=USER.email, context=..., ...)
    ```
    """
    def __init__(self):
        with open("./settings.json") as f:
            sett = json.load(f)
        
        self.email = sett["email"]
        self.language = sett["language"]
        self.language_audio = sett["language-audio"]
        self.language_text = sett["language-text"]
        self.username = sett["username"]
        self.paths = Path

class Path:
    def __init__(self):
        self.terminal = self._set_default_terminal_path()

    def _set_default_terminal_path(self) -> str:
        """
        Returns the default terminal path depending on the operating system
        """
        if platform.system() == "Windows":
            path = os.path.join(os.environ['USERPROFILE'])

        elif platform.system() in ["MacOS" ,"Linux"]:
            path = os.path.join(os.path.expanduser('~'))

        return path