import base64
import hashlib
import os
import random
import shutil
from typing import Optional

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import urllib3.util

from flux.core.helpers.commands import CommandInterface, Parser
from flux.utils import paths

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
        update_parser.add_argument("--from", help="use the specified URI to update flux (can also point to a file on disk)")

    def setup(self) -> None:

        if len(self.line_args) == 1:
            self.line_args.append("-h")

        if any(map(lambda x: x in self.line_args, ("-h", "--help"))):        
            self.print(self.banner())

        super().setup()

    def run(self):
        match self.args.command:
            case "update":
                self.flux_update()
    
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

    def flux_update(self):
        """
        update the flux application based on the version
        """

        update_manager = UpdateManager()
        update_manager.check_for_update(current_version=self.system.version, update_url=self.args.url)


class UpdateManager:

    def __init__(self, update_uri: Optional[str] = None):
        self.update_uri = update_uri
        self.latest_version: str = None
        self.download_url: str = None
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

    def verify_signature(self, file_path: str, signature_path: str, public_key_path: str) -> bool:
        """
        Verify the signature of the given file using the provided public key.

        `:returns` true if the signature verification passes, false otherwise
        `:raises` an error if unable to verify the signature
        """

        file_hash = self._compute_hash(file_path)

        # Write the computed hash to a temporary file
        hash_file_path = file_path + ".hash"
        with open(hash_file_path, "wb") as hash_file:
            hash_file.write(file_hash)

        with open(public_key_path, 'rb') as f:
            public_key = load_pem_public_key(f.read(), default_backend())

        with open(signature_path, 'rb') as f:
            # * the signature is base64 encoded
            signature = base64.b64decode(f.read())

        # verify the sigature
        try:
            res = public_key.verify(
                signature,
                file_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )

            return res or True
        except Exception:
            raise
        finally:
            os.remove(hash_file_path)

    def check_for_update(self, current_version: Optional[str] = None, update_url: Optional[str] = None) -> bool:
        """
        check the latest avaliable version of flux to determine if an update is available

        `:params` current_version: the current version of flux
        `:params` update_url: the path (url or local) used to determine if a newer version exists (if None, the default path will be used)
        `:returns` True if a possible update (or downgrade) has been detected
        `:raises` RuntimeError if it is not possible to update from the specified location
        """
        if not update_url:
            update_url = "https://api.github.com/repos/roysmanfo/flux/releases/latest"
        
        parsed_url = urllib3.util.parse_url(update_url)
        try:
            if paths.is_local_path(update_url):
                pass
            else:
                response = requests.get(update_url)

                if parsed_url.scheme.lower() not in  ("http://", "https://"):
                    raise RuntimeError("scheme '%s' is not supported for updates" % parsed_url.scheme)

                if parsed_url.host != "api.github.com":
                    raise RuntimeError("host '%s' is not supported for updates" % parsed_url.host)

                latest_release: dict = response.json()
                self.latest_version = latest_release["tag_name"]
                if self.latest_version != current_version:
                    self.download_url = latest_release["assets"][0]["browser_download_url"]
                    self.signature_url: str = self.download_url + ".sig"
                    return True
    
        except KeyError as e:
            raise KeyError(f"unable to retreave some informations: {e}" ) from e

        except requests.ConnectTimeout:
            raise TimeoutError(f"'{parsed_url.path}' does not seem respond in time: {e}" )

        except requests.ConnectionError as e:
            raise ConnectionError(f"unable to retreave some informations: {type(e)}" ) from e

        return False

    def get_update_info(self):
        """
        `:returns` a tuple containing (latest_version, download_url, signature_url)
        """

        return (self.latest_version, self.download_url, self.signature_url)

    def download_file(self, url: str, save_path: str) -> None:
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def uninstall_old_version(self, install_path: str) -> None:
        if os.path.exists(real_path := os.path.realpath(install_path)):
            # do not remove the root dir
            if real_path != os.path.realpath("/"):
                try:
                    shutil.rmtree(real_path)
                except PermissionError as e:
                    raise PermissionError("unable to uninstall old version in location '%s'" % real_path) from e

    def install_new_version(self, archive_path: str, install_path: str, *, uninstall_first: bool = True) -> None:
        if uninstall_first:
            self.uninstall_old_version(install_path)
        try:
            shutil.unpack_archive(filename=archive_path,
                                  extract_dir=install_path)
        except ValueError as e:
            raise ValueError("this file format is not unpackable (not supported)") from e
