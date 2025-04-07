from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)
from flux.core.manager import loader
from flux.utils import format
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

class Command(CommandInterface):
    """
    Help command to display information about available commands and their usage
    """

    def init(self) -> None:
        self.parser = Parser(prog="help", description="Display help information for available builtin commands")
        self.parser.add_argument(
            "command",
            nargs="*",
            help="The command to display help information for. If no command is provided, all commands will be listed"
        )

    def run(self) -> None:
        """
        Run the help command.
        """
        if self.args.command:
            command_names = self.args.command
        else:
            command_names = [command[:-3] for command in os.listdir(CUR_DIR) if command.endswith(".py") and command != "__init__.py"]

        command_names.sort()

        command_descriptions = {
            command: self.capitalize(self.get_description(command).strip()) for command in command_names
        }
        result_table = format.create_table(
            "command",
            "description",
            rows=command_descriptions.items(),
        )
        print(result_table)

    def get_description(self, command_name: str) -> str:
        """
        Get the description of the command.
        """
        command_instance = None
        try:
            command_class = loader.load_builtin_script(command_name)
            command_instance = command_class(system=self.system,
                               command=[],
                               is_process=False,
                               stdout=self.stdout,
                               stderr=self.stderr,
                               stdin=self.stdin,
                               privileges=self.system.privileges.LOW)
            command_instance.init()

            if command_instance.parser and command_instance.parser.description:
                return f"{command_instance.parser.description}"
            
            elif command_instance.__doc__:
                return f"{command_instance.__doc__.strip()}"
        
        except Exception as e:
            self.error(f"Error loading command {command_name}: {e}")
        
        finally:
            if command_instance:
                try:
                    command_instance.close()
                except Exception as e:
                    # self.error(f"Failed to close command instance: {e}")
                    pass

        # If no description is found, return a default message    
        return f"<no description available>"

    def capitalize(self, text: str) -> str:
        """
        Capitalize the first letter of the text.
        """
        return text[0].upper() + text[1:] if text else text
