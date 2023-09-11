"""
# `systemctl`
Allows the user to change different settings, such as the username or info.user.path informations
"""
from pathlib import Path
from ...helpers.arguments import Parser
from ...helpers.commands import *

class Commmand(CommandInterface):
    def init(self):
        self.parser = Parser(prog="systemctl", add_help=True,
                             description="Allows the user to change different settings, such as the username or info.user.path informations")
        self.parser.add_argument("-s", dest="setting", help="The setting to change")
        self.parser.add_argument("-v", dest="value", nargs="+", help="The new value of the setting to change (used with -s)")
        self.parser.add_argument("-r","--reset", dest="reset", action="store_true", help="Reset the selected setting to it's default value (used with -s)")
        self.parser.add_argument("--reset-all", dest="reset_all", action="store_true", help="Reset all settings")

    def run(self, command: list):
        """
        Handles which setting to change
        """
        self.args = self.parser.parse_args(command[1:])

        if self.parser.exit_execution:
            print()
            return

        if not self.args.reset_all:
            
            if not self.args.setting:
                self.error(STATUS_ERR, "The following arguments are required: -s")
                return
                
            if self.args.value and self.args.reset:
                self.error(STATUS_ERR, "Too many actions specified: -v, -r")
                return
                

        self.switch()

    def switch(self):
        """
        Assigns the input to the right function
        """

        # Reset all user vareables
        if self.args.reset_all:
            self.info.user.reset_settings()
            self.stdout.write('Restart the shell to apply changes\n')
            return

        # Change username
        if self.args.setting == "username":
            if self.args.value or self.args.reset:
                if len(self.args.value[0].strip()) > 1:
                    self.info.user.set_username("default" if self.args.reset else " ".join(self.args.value), self.info, self.args.reset)
                else:
                    self.stderr.write("The username provided is too short\n")
            else:
                self.stdout.write(f"{self.info.user.username}\n\n")

        # Set 1 or more new bg-task/s
        elif self.args.setting == "bg-task":
            if self.args.value or self.args.reset:
                self.info.user.set_bg_task(self.info, self.args.value, self.args.reset)
            else:
                self.stdout.write(f"{', '.join(self.info.user.background_tasks) if self.info.user.background_tasks else 'No background tasks'}\n\n")

        # Set/ change an email
        # if muliple emails given, set as email the first valid one
        elif self.args.setting == "email":
            if self.args.value or self.args.reset:
                self.info.user.set_email(self.info, self.args.value, self.args.reset)
            else:
                self.stdout.write(f"'{self.info.user.email}'\n\n")

        # change a Path
        elif self.args.setting.startswith("path"):
            if self.args.setting.startswith("path.") and len(self.args.setting.split(".")) == 2:
                target = self.args.setting.split(".")[1]
                if self.args.value or self.args.reset:
                    self.info.user.paths.set_path(target, Path("" if self.args.reset else self.args.value[0]), self.info, self.args.reset)
                else:
                    self.stdout.write(f"{self.info.user.paths.all()[target]}\n\n")
            else:
                from src.utils.format import create_table

                self.stdout.write(create_table("Path name", "Value", self.info.user.paths.all()))


        # Command does not exist
        else:
            self.error(STATUS_ERR, 'Setting not found')
