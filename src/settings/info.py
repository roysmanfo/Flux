import json
import os
import platform
import pathlib


with open("".join([os.path.dirname(os.path.realpath(__file__)), "\\version"])) as version:
    VERSION = version.read()

SETTINGS_FILE = pathlib.Path(
    "".join([os.path.dirname(os.path.realpath(__file__)), "\settings.json"]))
SETTINGS_FOLDER = pathlib.Path(
    "".join([os.path.dirname(os.path.realpath(__file__))]))


class Info:
    ...


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
            self.username: str = sett["username"]
            self.paths: Path = Path()
            self.background_tasks: list = BgTasks().tasks

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

    def set_username(self, new_username: str) -> None:
        self.username = new_username
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            settings['username'] = new_username
            with open(SETTINGS_FILE, "w") as l:
                l.write("")
                json.dump(settings, l, indent=4, sort_keys=True)

    def set_bg_task(self, info: Info, tasks: list):
        s = 0
        new_tasks = BgTasks()

        for task in tasks:
            if task in info.bg_tasks_available:
                if task not in info.user.background_tasks:
                    info.user.background_tasks.append(task)
                    new_tasks.add_task(task)
                    s = 1
                else:
                    print("This command is already a background task: " + task)
            else:
                print("This command is can't be converted to a background task: " + task)

        if s != 0:
            print('Changes will have effect on next startup')

            info.user.background_tasks = BgTasks().tasks


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

                    self.terminal: pathlib.Path = pathlib.Path(
                        path["terminal"]).resolve()
                    self.documents: pathlib.Path = pathlib.Path(
                        path["documents"]).resolve()
                    self.images: pathlib.Path = pathlib.Path(
                        path["images"]).resolve()
                    self.bucket: pathlib.Path = pathlib.Path(
                        path["bucket"]).resolve()
                    self.bucket_destination: pathlib.Path = pathlib.Path(
                        path["bucket-destination"]).resolve()

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

    def _set_default_terminal_path(self) -> pathlib.Path:
        """
        Returns the default terminal path depending on the operating system
        """
        path = pathlib.Path(os.path.join(os.path.expanduser('~')))
        return path

    def _set_default_documents_path(self) -> pathlib.Path:
        """
        Returns the location of the documents folder
        """
        path = pathlib.Path(os.path.join(os.path.expanduser('~'), 'Documents'))
        return path

    def _set_default_images_path(self) -> pathlib.Path:
        """
        Returns the location of the documents folder
        """
        path = pathlib.Path(os.path.join(os.path.expanduser('~'), "Pictures"))
        return path

    def _set_default_observer_bucket_path(self) -> pathlib.Path:
        """
        Returns the location of the observer's bucket folder
        """
        path = pathlib.Path(os.path.join(
            os.path.expanduser('~'), "Desktop", "Bucket"))
        return path

    def _set_default_observer_bucket_destination_path(self) -> pathlib.Path:
        """
        Returns the location of the observer's bucket destination folder
        """
        path = pathlib.Path(os.path.join(
            os.path.expanduser('~'), "Desktop", "Bucket", "Files"))
        return path


class BgTasks():
    def __init__(self):
        try:
            with open(SETTINGS_FILE, "r") as f:
                tasks = json.load(f)["background-tasks"]
                self.tasks: list = tasks
        except KeyError:
            self.reset()

    def reset(self) -> list:
        self.tasks = []

    def add_task(self, task: str):
        with open(SETTINGS_FILE, "r") as f:
            tasks: list = json.load(f)
            tasks["background-tasks"].append(task)
            with open(SETTINGS_FILE, "w") as l:
                # print(tasks)
                json.dump(tasks, l, indent=4, sort_keys=True)


class Info:
    """
    ### CLASS INFO

    This class contains every information a command may need.\n
    It's like a dictionary mapping information like the user instance or the version

    - user:                 The user instance
    - system_cmds:          A list off all commands that are built in the OS terminal
    - lang_file:            The lang_file path
    - settings_file:        The settings file path
    - settings_folder:      the settings folder path
    - version:              The software version number
    - bg_tasks:             A list of tasks which will be executes as background Threads
    - ignored_commands:     A list of commands which are ignored when called
    - bg_tasks_available:   All commands that are available to be "tasked"
    """

    def __init__(self,
                 user: User,
                 system_cmds: list,
                 bg_tasks: list,
                 ignored_commands: list,
                 bg_tasks_available: list
                 ):

        self.user = user
        self.system_cmds = system_cmds
        self.settings_file = SETTINGS_FILE
        self.settings_folder = SETTINGS_FOLDER
        self.version = VERSION
        self.bg_tasks = bg_tasks
        self.ignored_commands = ignored_commands
        self.bg_tasks_available = bg_tasks_available
