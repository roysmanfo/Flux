import base64
import hashlib
import os
from pathlib import Path
import random
import shutil
import asyncio
import re
import tarfile
import lzma
import math
from typing import Literal, Optional

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key 


from flux.core.helpers.commands import CommandInterface, Parser
from flux.utils import paths

PathOrStr = Path | str


ENTRY_POINT = "Flux"
EMOTES = [
    r"(ง ͠° ͟ل͜ ͡°)ง",
    r"(╯°□°)╯︵ ┻━┻",
    r"(ノಠ益ಠ)ノ彡┻━┻",
    r"┬─┬ノ( º _ ºノ)",
    r"¯\_(ツ)_/¯",
    r"( ͡◉ ͜ʖ ͡◉)",
    r"(  ಠ_ಠ )",
    r"(ꐦ ಠ皿ಠ )",
    r" ̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\з=(◣_◢)=ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿ ",
    r"ᕦ(⌐■ ͜ʖ■)ᕥ",
    r"\_(ಠ_ಠ)_/",
    r"┻━┻ ¯\_(ಠ□ಠ)_/¯ ┻━┻",
    r"(ノಠ益ಠ)ノ彡┻━┻ ლ(ಠ益ಠლ)",
]


class Flux(CommandInterface):

    def init(self):
        self.parser = Parser("flux", usage="flux [command] [options]")
        subparsers = self.parser.add_subparsers(title="commands", dest="command")
        update_parser = subparsers.add_parser("update", usage="flux update [options]", help="update flux to the most recent version")
        update_parser.add_argument("--from", dest="url", help="use the specified URI to update flux (can also point to a file on disk)")
        update_parser.add_argument("--skip-validation", action="store_true", help="do not verify the signature of the update (default: false)")

    def setup(self) -> None:

        if len(self.line_args) == 1:
            self.line_args.append("-h")

        if any(map(lambda x: x in self.line_args, ("-h", "--help"))):        
            self.print(self.banner())

        super().setup()

    def run(self):
        match self.args.command:
            case "update":
                asyncio.run(self.flux_update())

    def banner(self):
        emote = random.choice(EMOTES)
        banner_width = 38
        pad_len = max(0, (banner_width - len(emote)) // 2)
        pad = " " * pad_len
        emote = pad + emote
        title = fr"""
        {emote}
         ____       _____ __    __ __  __  __ 
        |    |___  |   __|  |  |  |  |\  \/  /
        |___|    | |   _]|  |__|  |  | |    | 
            |____| |__|  |_____\_____//__/\__\ 
                
        {'By @roysmanfo':^38}
        
        """
        return self.colors.Fore.LIGHTBLACK_EX + title + self.colors.Fore.RESET

    async def flux_update(self):
        """
        update the flux application based on the version
        """

        # needed for the backup before the update
        # backups are stored as: $HOME/.flux/.local/flux/backups/flux-{version}.tar.xz
        old_version_path = os.path.join(
            self.settings.syspaths.LOCAL_FOLDER,
            "flux",
            "backups",
            f"flux-{self.system.version}.tar.xz"
        )
        update_manager = UpdateManager(old_version_path=old_version_path)
        update_needed = update_manager.check_for_update(current_version=self.system.version, update_url=self.args.url)
        
        install_path = self.settings.syspaths.INSTALL_FOLDER
        
        # updates are (temp) stored in: $HOME/.flux/.cache/flux/updates/{update_file}
        archive_path = os.path.join(
            self.settings.syspaths.CACHE_FOLDER,
            "flux",
            "updates"
        )

        if update_needed:
            futures_res = await asyncio.gather(
                update_manager.download_update(archive_path),
                update_manager._create_backup(install_path),
                return_exceptions=True
            )
    
            if futures_res and (err := futures_res[0] or futures_res[1]):
                self.fatal(err)
                return

            # verify the update signature
            public_key = self.settings.syspaths.PUBLIC_KEY_FILE
            if not self.args.skip_validation and not update_manager.verify_signature(install_path, signature_path := "", public_key):
                self.warning("update signature verification failed (the signature ensures that updates are legit)")
                if self.input("update anyway? (y/N): ").lower() != "y":
                    self.warning("cancelling update...")
                    return
            
            await update_manager.install_new_version(archive_path, install_path, uninstall_first=True)

        else:
            asyncio.run(update_manager.install_new_version("", self.settings.syspaths.INSTALL_FOLDER, uninstall_first=True))
            # self.print("already up to date") <- uncoment once all test over here have been done


class UpdateManager:

    def __init__(self, update_uri: Optional[str] = None, *, old_version_path: str):
        self.update_uri = update_uri
        self.old_version_path = old_version_path
        self.latest_version: str = None
        self.download_url: str = None
        self.download_size: int = None
        self.signature_url: str = None

    def _compute_hash(self, file_path: str) -> bytes:
        """
        Compute the SHA-256 hash of the given file.
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.digest()      

    def _compare_versions(self, v1: str, v2: str) -> str:
        """
        Takes 2 flux versions as input and returns the most recent one
        """

        def _format_version(v: str):
            for segm in v.split('.'):
                if segm.isnumeric():
                    yield int(segm)
                else:
                    # may be something like x.y.z-dev
                    for i in segm.split('-'):
                        if i.isnumeric():
                            yield int(i)

        if (v1 := v1.strip()) == (v2 := v2.strip()):
            # same version
            return v1
        
        v1 = _format_version(v1)
        v2 = _format_version(v2)

        for i1, i2 in zip(v1, v2):
            if i1 > i2:
                return v1    
            elif i1 < i2:
                return v2

        # reaching here means that the 2 version are not homogeneus (ie. x.y and x.y.z)
        # they have same major (x) and minor (y) version, check for eventual micro version (z)

        if len(v1) > len(v2):
            return v1
        return v2

    def _convert_size(self, size_bytes: int, system: Literal["si", "iec"] = "iec") -> str:
        """
        Takes as input a number of bytes and converts them in the 
        most appropriate rappresentation (B, kiB, MiB or GiB)
        
        :param system: can be either "si" (kB = 1000 B) or (by default) "iec" (kB = 1024 B)
        """
        
        if size_bytes < 0:
            raise ValueError("byte number cannot be negative")
        if size_bytes == 0:
            return "0B"

        if system not in ("iec", "si"):
            raise ValueError("system `%s` is not supported" % system)
                
        size_name_si = ("B", "kB", "MB", "GB")
        size_name_iec = ("B", "kiB", "MiB", "GiB")
 
        unit = 1024 if system == "iec" else 1000
        size_name = size_name_iec if system == "iec" else size_name_si
        
        i = min(int(math.floor(math.log(size_bytes, unit))), len(size_name) - 1)
        p = math.pow(unit, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
            
    def verify_signature(self, file_path: str, signature_path: str, public_key_path: str) -> bool:
        """
        Verify the signature of the given file using the provided public key.

        - `:param` file_path: the location of the file to analize
        - `:param` signature_path: the signature created with the private key
        - `:param` public_key_path: the location of the public key

        `:returns` true if the signature verification passes, false otherwise
        """

        file_hash = self._compute_hash(file_path)

        with open(public_key_path, 'rb') as f:
            public_key = load_pem_public_key(f.read(), default_backend())

        with open(signature_path, 'rb') as f:
            signature = f.read()

            # ? is the signature base64 encoded (.sig) or not (.bin)
            if signature_path.endswith(".sig"):
                signature = base64.b64decode(signature)

        # verify the signature
        try:
            public_key.verify(
                signature,
                file_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except:
            return False

    def check_for_update(self, current_version: Optional[str] = None, update_url: Optional[str] = None) -> bool:
        """
        check the latest avaliable version of flux to determine if an update is available

        - `:params` current_version: the current version of flux
        - `:params` update_url: the path (url or local) used to determine if a newer version exists (if None, the default path will be used)
        
        `:returns` True if a possible update (or downgrade) has been detected

        `:raises` RuntimeError if a specific host or scheme is not supported (currently supported: http, https)  
        `:raises` KeyError if the response from the host does not contain some expected informations  
        `:raises` TimeoutError if the host does not respond in time  
        `:raises` ConnectionError for any other connection problem  
        """
        if not update_url:
            # this hardcoded value is just temporary,
            # a nicer way of handling this will be implemeted in the future
            update_url = "https://api.github.com/repos/roysmanfo/flux/releases/latest"

        parsed_url = paths.parse_url(update_url)

        try:
            if paths.is_local_path(update_url):
                self.download_url = update_url
                if not os.path.exists(update_url):
                    raise FileNotFoundError(update_url)
                self.download_size = os.path.getsize(update_url) if os.path.isfile(update_url) else 0
                self.signature_url: str = self.download_url + ".sig"
            else:
                if not parsed_url.scheme:
                    parsed_url.scheme = "https"
                
                if parsed_url.scheme not in  ("http", "https"):
                    raise RuntimeError("scheme '%s' is not supported for updates" % parsed_url.scheme)

                if parsed_url.host != "api.github.com":
                    raise RuntimeError("host '%s' is not supported for updates" % parsed_url.host)
                
                try:
                    accept = "application/json"
                    if "github.com" in parsed_url.host: 
                        accept = "application/vnd.github+json"

                    headers = {
                        "Accept": accept
                    }
                    verify_tsl = parsed_url.scheme == "https"
                    response = requests.get(parsed_url.url, headers=headers, timeout=3, verify=verify_tsl)
                    print(response.status_code, response.content)
                except requests.ConnectionError:
                    # possible SSL verification error, retry as a normal http request 
                    parsed_url.scheme = "http"
                    
                    # let possible errors be caught by the surrounding try-except block
                    response = requests.get(parsed_url.url, headers=headers, timeout=3, verify=verify_tsl)

                if response.status_code < 200 or response.status_code >= 400:
                    raise RuntimeError(f"{response.status_code} {response.reason}")

                latest_release: dict = response.json()
                self.latest_version = latest_release["tag_name"]
                if self.latest_version != current_version:
                    
                    # get the new release download url
                    assets = latest_release["assets"]
                    asset = assets[0] if assets else None
                    
                    if asset is None:
                        raise RuntimeError("no download url found")
                    
                    for a in assets:
                        if a != asset:
                            d_url: str = a["browser_download_url"]
                            if d_url.endswith('.tar.xz'):
                                asset = a

                    self.download_url = asset["browser_download_url"]
                    self.download_size = asset["size"]
                    self.signature_url: str = self.download_url + ".sig"
                    return True
    
        except KeyError as e:
            raise KeyError(f"unable to retreave some informations: {e}" ) from e

        except requests.ConnectTimeout:
            raise TimeoutError(f"'{parsed_url.path}' does not seem respond in time: {e}" )

        except requests.ConnectionError as e:
            raise ConnectionError(f"unable to retreave some informations: {type(e)}" ) from e

        except requests.JSONDecodeError as e:
            raise requests.JSONDecodeError(f"unable to retreave some informations: {e}" ) from e

        return False

    def get_update_info(self):
        """
        this method retutns some informations abount the fetched update 
        - the latest version available in the provided url to `check_for_update()`
        - the the actual download url to that version 
        - the path to the signature file of that version
        
        #### NOTE: call this AFTER `check_for_update()` or all values will default to None
        
        `:returns` a tuple containing (latest_version, download_url, signature_url)
        """

        return (self.latest_version, self.download_url, self.signature_url)

    async def download_update(self, save_path: PathOrStr) -> None:
        """
        downaload and save the update file(s)

        - `:param` save_path: the path where the download will be saved
        
        `:raises` RuntimeError `check_for_update()` has not been called or if `self.download_url` is None  
        `:raises` PermissionError if download_path or save_path are reserved paths (permission denied by the OS)
        """
        if not self.download_url:
            raise RuntimeError("self.download_url has not been set. Have you called `check_for_update()` first?")

        # may raise a PermissionError if a reserved path has been chosen
        if paths.is_local_path(self.download_url):
            if not os.path.isdir(save_path):
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            else:
                os.makedirs(save_path, exist_ok=True)
            try:
                shutil.copy(self.download_url, save_path)
            except shutil.SameFileError:
                # just use that file
                pass
        else:
            response = requests.get(self.download_url, stream=True)
            # may raise a PermissionError if a reserved path has been chosen
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)


    async def _create_backup(self, install_path: PathOrStr) -> None:
        def _file_filter(tarinfo: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
            rule = re.compile(r".*(\.pyc$|__pycache__|tmp_.*)")
            if re.search(rule, tarinfo.name):
                return None
            return tarinfo

        with lzma.LZMAFile(self.old_version_path, mode='w') as xz_file:
            with tarfile.open(mode='w', fileobj=xz_file) as tar_xz_file:
                tar_xz_file.add(install_path, filter=_file_filter)
        


    async def uninstall_old_version(self, install_path: PathOrStr) -> None:
        """
        removes the files of the old version from the system

        - `:param` install_path: the location of the older version to remove 
        
        `:raises` PermissionError if unable to uninstrall the old version 
        """
        if os.path.exists(real_path := os.path.realpath(install_path)):
            # do not remove the root dir
            if real_path != os.path.realpath("/"):
                try:
                    
                    # take the old version and compress it
                    # (just to have a backup in case of errors)
                    
                    if os.path.exists(self.old_version_path):

                        # remove old backup to replace it with a new one
                        if os.path.isdir(self.old_version_path):
                            shutil.rmtree(self.old_version_path)                   
                        else:
                            os.remove(self.old_version_path)
                    else:
                        os.makedirs(os.path.dirname(self.old_version_path), exist_ok=True)

                    # shutil.rmtree(real_path) <- un-comment once update is fully working
                    print(f"{self.old_version_path=}")
                    print(f"{real_path=}")
                except PermissionError as e:
                    raise PermissionError("unable to uninstall old version in location '%s'" % real_path) from e

    async def install_new_version(self, archive_path: PathOrStr, install_path: PathOrStr, *, uninstall_first: bool = False) -> None:
        """
        saves the new version on the system

        - `:param` archive_path: the location of the file downloaded with `download_update()`
        - `:param` install_path: the location of the old version (where to install the new version)
        - `:param` uninstall_first: before starting to install the new version, remove the old one (reccomended)
        
        `:raises` ValueError if unable to unpack the new version (archive format not supported)
        """
        if uninstall_first:
            await asyncio.gather(self.uninstall_old_version(install_path))
        # try:
        #     shutil.unpack_archive(filename=archive_path,
        #                           extract_dir=install_path)
        # except ValueError as e:
        #     raise ValueError("this file format is not unpackable (not supported)") from e
