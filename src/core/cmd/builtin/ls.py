"""
# `ls`

List information about the FILEs (the current directory by default).
"""

from ...helpers.commands import *
from ...helpers.arguments import Parser
import os
import stat
import time
from colorama import init as col_init, Fore, Back 
import zipfile

class Command(CommandInterface):

    def init(self):
        col_init(autoreset=True)
        self.parser = Parser(add_help=True, prog="ls", description="List information about the FILEs (the current directory by default).")
        self.parser.add_argument("PATH", nargs="?", default=self.info.user.paths.terminal, help="The path of the directory to list")
        self.parser.add_argument("-a", "--all", dest="all", action="store_true", help="Do not ignore entries starting with .")
        self.parser.add_argument("-l", dest="l", action="store_true", help="Use a long listing format")

    def run(self, command: list[str]):
        self.args = self.parser.parse_args(command[1:])

        if self.parser.exit_execution:
            print()
            return
        
        if not os.path.exists(self.args.PATH):
            self.error(STATUS_ERR, f"cannot access '{self.args.PATH}': No such file or directory")
            return
        
        dir_contents: list[str]

        if os.path.isdir(self.args.PATH) or os.path.ismount(self.args.PATH):
            self.args.PATH = os.path.abspath(self.args.PATH)
            try:
                dir_contents = os.listdir(self.args.PATH)
            except PermissionError:
                self.error(STATUS_ERR, f"cannot open `{self.args.PATH}` (permission denied)")
                return

        elif os.path.isfile(self.args.PATH) or os.path.islink(self.args.PATH):
            dir_contents = [self.args.PATH]

        #List all files
        if not self.args.all:
            dir_contents = [i for i in dir_contents if not i.startswith(".")]
        
        #Long listing format
        if self.args.l:
            if os.path.isfile(self.args.PATH):
                self.args.PATH = os.path.dirname(self.args.PATH)
            dir_contents = [self.long_listing_format(os.path.join(self.args.PATH, i)) for i in dir_contents]
            for file in dir_contents:
                self.stdout.write(file + "\n")
            self.stdout.write("\n\n")
            return
        
        output = []
        for content in dir_contents:
            complete_path = os.path.join(self.args.PATH, content)
            content = f"'{content}'" if len(str(content).split()) > 1 else content
            # Folder
            if os.path.isdir(complete_path):
                output.append(f"{Fore.LIGHTBLUE_EX}{content}")
            # Image
            elif content.removesuffix("'").split(".")[-1].lower() in ['jpg', 'jpeg', 'tif', 'jfif', 'png', 'gif', 'bmp', 'webp', 'pdf']:
                output.append(f"{Fore.LIGHTMAGENTA_EX}{content}")
            # Executable
            elif sys.platform.lower().startswith("win") and "." + content.removesuffix("'").split(".")[-1].upper() in os.environ['PATHEXT']:
                output.append(f"{Back.LIGHTYELLOW_EX} {Fore.BLACK}{content} {Back.RESET}")
            # Compressed archive
            elif zipfile.is_zipfile(content):
                output.append(f"{Fore.LIGHTRED_EX}{content}")
            # Regular file
            else:
                output.append(f"{Fore.LIGHTGREEN_EX}{content}")

        max_line_length = os.get_terminal_size().columns // 4 * 3
        linelenght = 0
        for content in output:
            if linelenght + len(content) + 2 < (max_line_length):
                self.stdout.write(f"{content}  ")
                linelenght += len(content) + 2
            else:
                linelenght = len(content) + 2
                self.stdout.write(f"\n{content}  ")

        self.stdout.write("\n\n")
    
    
    @staticmethod
    def long_listing_format(file_path: str) -> str:
        def get_permissions_string(mode):
            permissions = {
                stat.S_IRUSR: 'r', stat.S_IWUSR: 'w', stat.S_IXUSR: 'x',
                stat.S_IRGRP: 'r', stat.S_IWGRP: 'w', stat.S_IXGRP: 'x',
                stat.S_IROTH: 'r', stat.S_IWOTH: 'w', stat.S_IXOTH: 'x'
            }
            mode_str = ''
            for mask, perm_char in permissions.items():
                mode_str += perm_char if mode & mask else '-'
            return mode_str

        def format_file_info(file_info: os.stat_result):
            mode = file_info.st_mode
            permissions = get_permissions_string(mode)
            size = file_info.st_size
            modified_time = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))
            return f"{permissions} {size:8} {modified_time}"

        file_info: os.stat_result = os.stat(file_path)

        formatted_info = format_file_info(file_info)

        # Color formatting

        # Folder
        if os.path.isdir(file_path):
            formatted_info += f" {Fore.LIGHTBLUE_EX}{os.path.basename(file_path)}"
        # Image
        elif file_path.removesuffix("'").split(".")[-1].lower() in ['jpg', 'jpeg', 'tif', 'jfif', 'png', 'gif', 'bmp', 'webp', 'pdf']:
            formatted_info +=  f" {Fore.LIGHTMAGENTA_EX}{os.path.basename(file_path)}"
        # Executable
        elif sys.platform.lower().startswith("win") and "." + file_path.removesuffix("'").split(".")[-1].upper() in os.environ['PATHEXT']:
            formatted_info += f" {Back.LIGHTYELLOW_EX}{Fore.BLACK}{os.path.basename(file_path)}{Back.RESET}"
        # Compressed archive
        elif zipfile.is_zipfile(file_path):
            formatted_info += f" {Fore.LIGHTRED_EX}{os.path.basename(file_path)}"
        # regular file
        else:
            formatted_info += f" {Fore.LIGHTGREEN_EX}{os.path.basename(file_path)}"

        return formatted_info

