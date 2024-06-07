import json
import os
import pathlib
import platform
from typing import List
from enum import Enum 

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'version'), mode='r', encoding='utf-8') as version:
    VERSION = version.read()

_pathlib_class_type = type(pathlib.Path()) # PosixPath or WindowsPath

class SysPaths(_pathlib_class_type, Enum):
    CONFIG_FOLDER = pathlib.Path(os.path.join(os.path.expanduser("~"), ".flux")).resolve()
    SETTINGS_FILE = pathlib.Path(os.path.join(CONFIG_FOLDER, "settings.json")).resolve()
    SETTINGS_FOLDER = pathlib.Path(os.path.dirname(SETTINGS_FILE)).resolve()
    CACHE_FOLDER = pathlib.Path(os.path.join(CONFIG_FOLDER, "cache")).resolve()
    LOCAL_FOLDER = pathlib.Path(os.path.join(CONFIG_FOLDER, ".local")).resolve()
    
    def __str__(self):
        return str(self.value)
    
    @staticmethod
    def create_initial_folders() -> None:
        """
        You should check for permission when creatin an object of this class

        It is not to take for granted that we have write permission on `~`

        `:raises` PermissionError if we do not have permissions to write in a folder
        """
        try:
            for i in SysPaths:
                if i._name_.upper().endswith("FOLDER"):
                    os.makedirs(i.value, exist_ok=True)
            
        except OSError as e:
            raise PermissionError(e.__str__()) # raise a more descriptive exception

    def copy(self):
        return SysPaths()


class Settings:
    ...


class User():
    """
    ### CLASS USER
    The class User manages all user info and settings, plus this
    approach makes working with user properties much easier than in
    the previus version of Flux, where all settings where also stored
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
            with open(SysPaths.SETTINGS_FILE, "r", encoding='utf-8') as f:
                sett = json.load(f)

            self.email: str = sett["email"]
            self.username: str = sett["username"]
            self.paths: Path = Path()

        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            self.reset_settings()
            self.__init__()

    def copy(self):
        user = User()
        
        user.email = self.email
        user.username = self.username
        user.paths = self.paths.copy()
        
        return user

    def reset_settings(self) -> None:
        """
        ### Reset Settings
        This method resets the default settings, and also checks if the settings
        file is already there, if there already is one, it gets overwritten, otherwise
        a new one is created.
        """

        # Create the settings file
        with open(SysPaths.SETTINGS_FILE, "w", encoding='utf-8') as file:
            file.write("{}")

        path = Path(False)

        settings = {
            "email": "",
            "username": os.path.basename(os.path.expanduser('~')),
            "paths": path.reset(),
        }

        # Check if there already is a settings file, if there is, overwrite it, otherwise
        # create a new one

        with open(SysPaths.SETTINGS_FILE, "w", encoding='utf-8') as l:
            l.write("")
            json.dump(settings, l, indent=4, sort_keys=True)

    def set_username(self, new_username: str, info: Settings, reset: bool = False) -> None:
        """
        Sets the username to new_username
        """
        if reset:
            new_username = os.path.basename(os.path.expanduser('~'))

        info.user.username = new_username
        with open(SysPaths.SETTINGS_FILE, "r", encoding='utf-8') as f:
            settings = json.load(f)
            settings['username'] = new_username
            with open(SysPaths.SETTINGS_FILE, "w", encoding='utf-8') as l:
                l.write("")
                json.dump(settings, l, indent=4, sort_keys=True)

    def set_email(self, info: Settings, emails: List[str], reset: bool = False):
        """
        Change the user email to the first valid email address in @param emails
        """
        if reset:
            info.user.email = ""
            with open(SysPaths.SETTINGS_FILE, "r", encoding='utf-8') as f:
                sett: list = json.load(f)
                sett["email"] = info.user.email
                with open(SysPaths.SETTINGS_FILE, "w", encoding='utf-8') as l:
                    json.dump(sett, l, indent=4, sort_keys=True)

            print("Email changed to: ''")
            return

        for email in emails:
            is_valid_email = True
            email.strip()

            if email.startswith('$'):
                var = email
                email = info.variables.get(
                    email.removeprefix('$'), None).strip()

                if email is None:

                    info.no_var_found(var)
                    is_valid_email = False

            elif email.count("@") != 1:
                is_valid_email = False

            elif email.count(" ") != 0:
                is_valid_email = False

            elif len(email.split(".")[-1]) < 2:
                is_valid_email = False

            if is_valid_email:

                # Update the email
                info.user.email = email
                with open(SysPaths.SETTINGS_FILE, "r", encoding='utf-8') as f:
                    sett: list = json.load(f)
                    sett["email"] = email
                    with open(SysPaths.SETTINGS_FILE, "w", encoding='utf-8') as l:
                        json.dump(sett, l, indent=4, sort_keys=True)

                print("Email changed to: ", email)
                return
            else:
                print("This email is not a valid one: ", email)


class Path:
    """
    ### CLASS PATH

    The class Path contains all different infornamtion about where to find many
    different things, like where to put files, or where to look for them

    @param load_data : If set to False, the object will not have any path loaded
    """

    def __init__(self, load_data: bool = True):
        if not load_data:
            return

        try:
            with open(SysPaths.SETTINGS_FILE, "r", encoding='utf-8') as f:
                path: dict = json.load(f)["paths"]
                self.all_paths = path.copy()

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

    def copy(self):
        paths = Path(False)
        paths.terminal = self.terminal
        paths.documents = self.documents
        paths.images = self.images
        paths.bucket = self.bucket
        paths.bucket_destination = self.bucket_destination
        return paths

    def all(self) -> dict:
        """
        Returns a dictionary of all Paths in the settings file
        with deir current value
        """
        paths = {
            "terminal": self.terminal,
            "documents": self.documents,
            "images": self.images,
            "bucket": self.bucket,
            "bucket-destination": self.bucket_destination
        }
        return paths

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
        if platform.system().lower().startswith("win"):
            return pathlib.Path(os.path.join(os.path.expanduser('~'), "Desktop", "Bucket"))

        return pathlib.Path(os.path.join(os.path.expanduser('~'), "bucket"))

    def _set_default_observer_bucket_destination_path(self) -> pathlib.Path:
        """
        Returns the location of the observer's bucket destination folder
        """
        if platform.system().lower().startswith("win"):
            return pathlib.Path(os.path.join(os.path.expanduser('~'), "Desktop", "Bucket", "Files"))

        return pathlib.Path(os.path.join(os.path.expanduser('~'), "bucket", "files"))
        

    def set_path(self, target: str, new_path: pathlib.Path, info: Settings, reset: bool = False) -> None:
        """
        Changes the specified path
        """
        new_path = info.variables.get(str(new_path).removeprefix(
            "$")) if str(new_path).startswith("$") else new_path

        new_path = pathlib.Path(new_path).resolve(strict=True)

        if target == "bucket":
            self.bucket = new_path if not reset else self._set_default_observer_bucket_path()
            new_path = new_path if not reset else self._set_default_observer_bucket_path()
        elif target == "bucket-destination":
            self.bucket_destination = new_path if not reset else self._set_default_observer_bucket_destination_path()
            new_path = new_path if not reset else self._set_default_observer_bucket_destination_path()
        elif target == "documents":
            self.documents = new_path if not reset else self._set_default_documents_path()
            new_path = new_path if not reset else self._set_default_documents_path()
        elif target == "images":
            self.images = new_path if not reset else self._set_default_images_path()
            new_path = new_path if not reset else self._set_default_images_path()
        elif target == "terminal":
            self.terminal = new_path if not reset else self._set_default_terminal_path()
            new_path = new_path if not reset else self._set_default_terminal_path()
        else:
            print("Invalid setting specified")
            return

        if not new_path.exists():
            try:
                os.makedirs(new_path, exist_ok=True)
            except PermissionError:
                print(f"Permission denied to create {new_path}")
                return

        with open(SysPaths.SETTINGS_FILE, "r", encoding='utf-8') as f:
            tasks: dict = json.load(f)
            tasks["paths"][target] = str(new_path)
            with open(SysPaths.SETTINGS_FILE, "w", encoding='utf-8') as l:
                json.dump(tasks, l, indent=4, sort_keys=True)
        print(f"Successfully changed path.{target} to {new_path}\n")


class Settings:
    """
    ### CLASS SETTINGS

    This class contains every information a command may need.\n
    It's like a dictionary mapping information like the user instance or the version

    - user:                 The user instance
    - syspaths:             A collection of paths reserved to flux and flux commands
    """

    def __init__(self, user: User):

        self.user = user
        self.syspaths = SysPaths

    def copy(self):
        """
        Returns a copy of the current state of Info
        """
        return Settings(self.user.copy(), self.syspaths.copy())

