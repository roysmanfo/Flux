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
  -v VALUE          The new value of the setting to change
  -r, --reset       Reset the selected setting to it's default value (commbined with -s)
  --reset-all       Reset all settings
""")

    def run(self, command: list, info: object):
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
                if not self.args.value and not self.args.reset:
                    self.parser.help()
                    return

                self.parser.exit(2, "error: the following arguments are required: -s")

            if not self.args.value:
                if not self.args.reset:
                    self.parser.exit(
                        2, "error: the following arguments are required: -v")
                    return

        self.switch(info)

    def switch(self, info: object):
        """
        Assigns the input to the right function
        """

        # Reset all user vareables
        if self.args.reset_all:
            info.user.reset_settings()
            print('Restart the shell to apply changes')
            return

        # Change username
        if self.args.setting == "username":
            if len(self.args.value[0]) > 1:
                info.user.set_username(self.args.value[0], info)
            else:
                print("The username provided is too short")

        # Set 1 or more new bg-task/s
        elif self.args.setting == "bg-task":
            info.user.set_bg_task(info, self.args.value)

        # Set/ change an email
        # if muliple emails given, set as email the first valid one
        elif self.args.setting == "email":
            info.user.set_email(info, self.args.value)

        # change a Path
        elif self.args.setting.startswith("path.") and len(self.args.setting.split(".")) == 2:
            target = self.args.setting.split(".")[1]
            info.user.paths.set_path(target, Path("" if self.args.reset else self.args.value[0]), info, self.args.reset)

        # Command does not exist
        else:
            print('Command not found')
