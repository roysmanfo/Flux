"""
# `settings`
Allows the user to change different settings, such as the username or info.user.path informations
"""
from pathlib import Path
from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="settings",
                             description="Allows the user to change different settings, such as the username or info.user.path informations")
        self.parser.add_argument("setting", nargs="?", help="The setting to change")
        self.parser.add_argument("-v", dest="value", nargs="+", help="The new value of the setting to change (used with -s)")
        self.parser.add_argument("-r","--reset", dest="reset", action="store_true", help="Reset the selected setting to it's default value (used with -s)")
        self.parser.add_argument("--reset-all", dest="reset_all", action="store_true", help="Reset all settings")

    def run(self):
        """
        Handles which setting to change
        """

        if not self.args.reset_all:
            
            if not self.args.setting:
                self.error(self.errors.parameter_not_specified("setting"))
                return
                
            if self.args.value and self.args.reset:
                self.error("Too many actions specified: -v, -r")
                return
                

        self.switch()

    def switch(self):
        """
        Assigns the input to the right function
        """

        # Reset all user vareables
        if self.args.reset_all:
            self.settings.user.reset_settings()
            self.print('Restart the shell to apply changes')
            return
        
        self.args.setting = str(self.args.setting) # this is just for intellisense
        
        # Change username
        if self.args.setting == "username":
            if self.args.value or self.args.reset:
                if len(self.args.value[0].strip()) > 1:
                    self.settings.user.set_username("default" if self.args.reset else " ".join(self.args.value), self.settings, self.args.reset)
                else:
                    self.stderr.write("The username provided is too short\n")
            else:
                self.print(f"{self.settings.user.username}\n")

        # Set/ change an email
        # if muliple emails given, set as email the first valid one
        elif self.args.setting == "email":
            if self.args.value or self.args.reset:
                self.settings.user.set_email(self.settings, self.args.value, self.args.reset)
            else:
                self.print(f"'{self.settings.user.email}'\n")

        # change a Path
        elif self.args.setting.startswith("path"):
            if self.args.setting.startswith("path.") and len(self.args.setting.split(".")) == 2:
                target = self.args.setting.split(".")[1]
                if self.args.value or self.args.reset:
                    if self.args.value[0] and Path(self.args.value[0]).exists():
                        self.settings.user.paths.set_path(target, Path("" if self.args.reset else self.args.value[0]), self.settings, self.args.reset)
                    else:
                        self.error(self.errors.file_not_found(self.args.value[0]))
                else:
                    try:
                        self.print(f"{self.settings.user.paths.all()[target]}\n")
                    except KeyError:
                        self.error(f"setting not found")
            else:
                from flux.utils.tables import create_table
                c = [(p, self.settings.user.paths.all_paths[p]) for p in self.settings.user.paths.all_paths.keys()]
                
                self.print(create_table("Path name", "Value", rows=c))


        # Command does not exist
        else:
            self.error('setting not found')
