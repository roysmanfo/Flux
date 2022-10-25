import json, os, platform

class User():
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