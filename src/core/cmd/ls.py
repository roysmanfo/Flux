from .helpers.commands import *
from .helpers.arguments import Parser
import os
import stat
import time
from colorama import init as col_init, Fore, Back 

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

        dir_contents = os.listdir(self.args.PATH)

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

        output = ""
        for content in dir_contents:
            if os.path.isdir(content):
                output += f"{Fore.LIGHTBLUE_EX}{content}  "
            elif os.path.isfile(content):
                output += f"{Fore.CYAN}{content}  "

        self.stdout.write(output + "\n\n")
    
    
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
            user = file_info.st_uid
            group = file_info.st_gid
            size = file_info.st_size
            modified_time = time.strftime("%b %d %H:%M", time.localtime(file_info.st_mtime))
            return f"{permissions} {user} {group} {size:8} {modified_time}"
        
        file_info: os.stat_result = os.stat(file_path)

        formatted_info = format_file_info(file_info)
        
        if os.path.isdir(file_path):
            formatted_info += f" {Fore.LIGHTBLUE_EX}{os.path.basename(file_path)}"
        else:
            formatted_info += f" {Fore.LIGHTGREEN_EX}{os.path.basename(file_path)}"


        return formatted_info


