"""
# `ls`

List information about the FILEs (the current directory by default).
"""

from typing import List
from flux.core.helpers.commands import (
    CommandInterface,
    Parser,
    Status
)
from flux.utils import tables

import sys
import os
import stat
import time
import zipfile

class Command(CommandInterface):

    def init(self):
        self.parser = Parser(prog="ls", description="List information about the FILEs (the current directory by default).")
        self.parser.add_argument("PATH", nargs="?", default=".", help="The path of the directory to list")
        self.parser.add_argument("-a", "--all", action="store_true", help="do not ignore entries starting with .")
        self.parser.add_argument("-A", "--almost-all", action="store_true", help="do not list implied . and ..")
        self.parser.add_argument("-d", "--directory", action="store_true", help="list directories themselves, not their contents")
        self.parser.add_argument("-r", "--reverse", action="store_true", help="reverse order while sorting")
        self.parser.add_argument("-l", dest="l", action="store_true", help="use a long listing format")

    def run(self):

        if not os.path.exists(self.args.PATH):
            self.error(f"cannot access '{self.args.PATH}': No such file or directory")
            return
        
        dir_contents: List[str] = []
        
        if self.args.directory or os.path.isfile(self.args.PATH) or os.path.islink(self.args.PATH):
            dir_contents = [self.args.PATH] 
        
        elif os.path.isdir(self.args.PATH) or os.path.ismount(self.args.PATH):
            self.args.PATH = os.path.abspath(self.args.PATH)
            try:
                dir_contents = os.listdir(self.args.PATH)
            except PermissionError:
                self.error(f"cannot open `{self.args.PATH}` (permission denied)")
                return
        else:
            # wtf is this path pointing to
            pass


        #List all files
        if not self.args.directory:
            if not self.args.all:
                dir_contents = [i for i in dir_contents if not i.startswith(".")]
            elif not self.args.almost_all:
                dir_contents.insert(0, "..")
                dir_contents.insert(0, ".")
        
        if self.args.reverse:
            dir_contents = dir_contents[::-1]

        #Long listing format
        if self.args.l:
            if os.path.isfile(self.args.PATH):
                self.args.PATH = os.path.dirname(self.args.PATH)
            dir_contents = [self.long_listing_format(os.path.join(self.args.PATH, i)) for i in dir_contents]

            self.print()        
            for file in dir_contents:
                if file:
                    self.print(file)
            self.print("\n")
            return
        
        output = []
        for content in dir_contents:
            complete_path = os.path.join(self.args.PATH, content)
            content = f"'{content}'" if len(str(content).split()) > 1 else content
            # Folder
            if os.path.isdir(complete_path):
                output.append(f"{self.colors.Fore.LIGHTBLUE_EX}{content}{self.colors.Fore.RESET}")
            # Image
            elif content.removesuffix("'").split(".")[-1].lower() in ['jpg', 'jpeg', 'tif', 'jfif', 'png', 'gif', 'bmp', 'webp', 'pdf']:
                output.append(f"{self.colors.Fore.LIGHTMAGENTA_EX}{content}{self.colors.Fore.RESET}")
            # Executable
            elif sys.platform.lower().startswith("win") and "." + content.removesuffix("'").split(".")[-1].upper() in os.environ['PATHEXT']:
                output.append(f"{self.colors.Fore.LIGHTYELLOW_EX}{content}{self.colors.Fore.RESET}")
            # Compressed archive
            elif zipfile.is_zipfile(content):
                output.append(f"{self.colors.Fore.LIGHTRED_EX}{content}{self.colors.Fore.RESET}")
            # Regular file
            else:
                output.append(f"{self.colors.Fore.LIGHTGREEN_EX}{content}{self.colors.Fore.RESET}")

        # max_line_length = os.get_terminal_size().columns // 4 * 3
        # linelenght = 0
        # for content in output:
        #     if linelenght + len(content) + 2 < (max_line_length):
        #         self.print(f"{content}  ", end="")
        #         linelenght += len(content) + 2
        #     else:
        #         linelenght = len(content) + 2
        #         self.print(f"\n{content}  ", end="")
        self.print(tables.create_adaptive_table(output))    
    
    def long_listing_format(self, file_path: str) -> str:
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
            try:
                mode = file_info.st_mode
                permissions = get_permissions_string(mode)
                size = file_info.st_size
                modified_time = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))
                return f"{permissions} {size:9} {modified_time}"
            
            except OSError: # no permissions
                return None

        file_info: os.stat_result = os.stat(file_path)

        formatted_info = format_file_info(file_info)

        # Color formatting
        if formatted_info:
            # Folder
            if os.path.isdir(file_path):
                formatted_info += f" {self.colors.Fore.LIGHTBLUE_EX}{os.path.basename(file_path)}"
            # Image
            elif file_path.removesuffix("'").split(".")[-1].lower() in ['jpg', 'jpeg', 'tif', 'jfif', 'png', 'gif', 'bmp', 'webp', 'pdf']:
                formatted_info +=  f" {self.colors.Fore.LIGHTMAGENTA_EX}{os.path.basename(file_path)}"
            # Executable
            elif sys.platform.lower().startswith("win") and "." + file_path.removesuffix("'").split(".")[-1].upper() in os.environ['PATHEXT']:
                formatted_info += f" {self.colors.Fore.LIGHTYELLOW_EX}{os.path.basename(file_path)}{self.colors.Fore.RESET}"
            # Compressed archive
            elif zipfile.is_zipfile(file_path):
                formatted_info += f" {self.colors.Fore.LIGHTRED_EX}{os.path.basename(file_path)}"
            # regular file
            else:
                formatted_info += f" {self.colors.Fore.LIGHTGREEN_EX}{os.path.basename(file_path)}"

            return formatted_info
        self.printerr(self.errors.cannot_read_fod(file_path.rstrip("\n")))
        self.status = Status.STATUS_ERR
        return ""
