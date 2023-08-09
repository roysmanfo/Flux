"""
# `set`
Allows the user to change different settings, such as the username or info.user.path informations
"""
from pathlib import Path
from .helpers.arguments import Parser
from .helpers.commands import CommandInterface

OPTIONS = []
FLAGS = ['--reset', '--all']


class Commmand(CommandInterface):
    def init(self):
        self.parser = Parser(prog="set",
                             description="Allows the user to change different settings, such as the username or info.user.path informations")
        self.parser.add_argument("-s", dest="setting")
        self.parser.add_argument("-v", dest="value", nargs="+")
        self.parser.add_argument("-r","--reset", dest="reset", action="store_true")
        self.parser.add_argument("--reset-all", dest="reset_all", action="store_true")
        self.parser.add_help_message("""Allows the user to change different settings, such as the username or info.user.path informations
                                     
usage: set [-h] [--reset-all] -s SETTING [--reset][-v VALUE]

options:
  -h, --help        Show this help message
  -s SETTING        The setting to change
  -v VALUE          The new value of the setting to change (used with -s)
  -r, --reset       Reset the selected setting to it's default value (used with -s)
  --reset-all       Reset all settings
""")

    def run(self, command: list):
        """
        Handles which setting to change
        """
        self.args = self.parser.parse_args(command[1:])

        if self.parser.exit_execution:
            return

        if self.args.help:
            self.parser.help()
            return

        if not self.args.reset_all:
            
            if not self.args.setting:
                if not self.args.value or not self.args.reset:
                    self.parser.help()
                    self.parser.exit(2, "error: the following arguments are required: -s\n")
                    return


            if not self.args.value:
                if not self.args.reset:
                    self.parser.exit(2, "error: one of the following arguments is required: -v, -r\n")
                    return

        self.switch()

    def switch(self):
        """
        Assigns the input to the right function
        """

        # Reset all user vareables
        if self.args.reset_all:
            self.info.user.reset_settings()
            print('Restart the shell to apply changes')
            return

        # Change username
        if self.args.setting == "username":
            if len(self.args.value) > 0 and len(self.args.value[0].strip()) > 1:
                self.info.user.set_username("" if self.args.reset else " ".join(self.args.value), self.info, self.args.reset)
            else:
                print("The username provided is too short")

        # Set 1 or more new bg-task/s
        elif self.args.setting == "bg-task":
            self.info.user.set_bg_task(self.info, self.args.value, self.args.reset)

        # Set/ change an email
        # if muliple emails given, set as email the first valid one
        elif self.args.setting == "email":
            self.info.user.set_email(self.info, self.args.value, self.args.reset)

        # change a Path
        elif self.args.setting.startswith("path.") and len(self.args.setting.split(".")) == 2:
            target = self.args.setting.split(".")[1]
            self.info.user.paths.set_path(target, Path("" if self.args.reset else self.args.value[0]), self.info, self.args.reset)

        # Command does not exist
        else:
            print('Setting not found\n')
