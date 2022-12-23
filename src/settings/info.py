import json
import os
import platform


with open("".join([os.path.dirname(os.path.realpath(__file__)), "\\version"])) as version:
    VERSION = version.read()

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

    #### Example: 
    >>> send_email = lambda sender: str, context: dict, ... : ... #some code to send a mail
    >>> send_email(sender=USER.email, context=..., ...)

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
            self.paths: Path = Path()
            self.background_tasks: BgTasks = BgTasks()

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
        bg_tasks = BgTasks(self)

        settings = {
            "email": "",
            "language": "en",
            "language-audio": "en",
            "language-text": "en",
            "username": "User",
            "paths": path.reset(),
            "background-tasks": bg_tasks.reset(),
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

    def __init__(self, load_data: bool = True):
        if load_data:
            try:
                with open(SETTINGS_FILE, "r") as f:
                    path = json.load(f)["paths"]

                    self.terminal: str = path["terminal"]
                    self.documents: str = path["documents"]
                    self.images: str = path["images"]
                    self.bucket: str = path["bucket"]
                    self.bucket_destination: str = path["bucket-destination"]

            except KeyError:
                self.reset()

    def reset(self) -> dict:
        """
        Returns a dictionary containing all the default paths to look for
        """
        self.terminal = self._set_default_terminal_path()
        self.documents = self._set_default_documents_path()
        self.images = self._set_default_images_path()
        self.bucket = self._set_default_observer_bucket_path()
        self.bucket_destination = self._set_default_observer_bucket_destination_path()

        all_paths = {
            "terminal": f"{self.terminal}",
            "documents": f"{self.documents}",
            "images": f"{self.images}",
            "bucket": f"{self.bucket}",
            "bucket-destination": f"{self.bucket_destination}",
        }

        return all_paths

    def all(self) -> dict:
        paths = {
            "terminal": self.terminal,
            "documents": self.documents,
            "images": self.images,
            "bucket": self.bucket,
            "bucket-destination": self.bucket_destination
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

    def _set_default_observer_bucket_path(self) -> str:
        """
        Returns the location of the observer's bucket folder
        """
        path = "/".join([os.path.expanduser('~'), "Desktop", "Bucket"])
        if "\\" in path:
            return path.replace("\\", "/")
        else:
            return path

    def _set_default_observer_bucket_destination_path(self) -> str:
        """
        Returns the location of the observer's bucket destination folder
        """
        path = "/".join([os.path.expanduser('~'),
                        "Desktop", "Bucket", "Files"])
        if "\\" in path:
            return path.replace("\\", "/")
        else:
            return path


class BgTasks():
    def __init__(self):
        try:
            with open(SETTINGS_FILE, "r") as f:
                tasks = json.load(f)["background'tasks"]
                self.tasks: list = tasks
        except KeyError:
            self.reset()

    def reset(self) -> list:
        return []
