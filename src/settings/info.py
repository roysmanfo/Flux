import json
import os
import platform

SETTINGS_FILE = "".join(
    [os.path.dirname(os.path.realpath(__file__)), "\settings.json"])
SETTINGS_FOLDER = "".join([os.path.dirname(os.path.realpath(__file__))])


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
        try:
            with open(SETTINGS_FILE, "r") as f:
                sett = json.load(f)

            self.email: str = sett["email"]
            self.language: str = sett["language"]
            self.language_audio: str = sett["language-audio"]
            self.language_text: str = sett["language-text"]
            self.username: str = sett["username"]
            self.paths: dict = sett["paths"]

        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            self.reset_settings()
            self.__init__()

    def reset_settings(self) -> None:
        """
        ### Reset Settings
        This method resets the default settings, and also checks if the settings
        file is already there, if there already is one, it gets overwritten, otherwise
        a new one is created.
        """
        path = Path(self, False)

        settings = {
            "email": "",
            "language": "en",
            "language-audio": "en",
            "language-text": "en",
            "username": "",
            "paths": path.reset()
        }

        # Check if there already is a settings file, if there is, overwrite it, otherwise
        # create a new one
        try:

            with open(SETTINGS_FILE, "r") as f:
                with open(SETTINGS_FILE, "w") as l:
                    l.write("")
                    json.dump(settings, l, indent=4, sort_keys=True)
        except FileNotFoundError:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=4, sort_keys=True)


class Path:
    """
    ### CLASS PATH
    The class Path contains all different infornamtion about where to find many
    different things, like where to put files, or where to look for them
    """

    def __init__(self, user: User, load_data: bool = True):
        if load_data:
            try:
                with open(SETTINGS_FILE, "r") as f:
                    path = json.load(f)["paths"]

                    self.terminal: str = path["terminal"]
                    self.documents: str = path["documents"]
            except KeyError:
                user.reset_settings()
                self.__init__(user=user, load_data=True)

    def reset(self) -> dict:
        """
        Returns a dictionary containing all the default paths to look for
        """
        self.terminal = self._set_default_terminal_path()
        self.documents = self._set_default_documents_path()
        self.images = self._set_default_images_path()

        all_paths = {
            "terminal": f"{self.terminal}",
            "documents": f"{self.documents}",
        }

        return all_paths

    def all(self) -> dict:
        paths = {
            "terminal": self.terminal,
            "documents": self.documents,
        }
        return sorted(paths)

    def _set_default_terminal_path(self) -> str:
        """
        Returns the default terminal path depending on the operating system
        """
        if platform.system() == "Windows":
            path = os.path.join(os.environ['USERPROFILE'])

        elif platform.system() in ["MacOS", "Linux"]:
            path = os.path.join(os.path.expanduser('~'))
        if "\\" in path:
            return path.replace("\\", "/")
        else:
            return path

    def _set_default_documents_path(self) -> str:
        """
        Returns the location of the documents folder
        """
        path = "/".join([self.terminal, 'Documents'])
        return path

    def _set_default_images_path(self) -> str:
        """
        Returns the location of the documents folder
        """
        path = "/".join([self.terminal, 'Documents'])
        return path
