from ...helpers.commands import *
from ...helpers.arguments import Parser


COMMANDS_AVAILABLE = [
    'install',
    'purge',
    'update',
    'upgrade',
    'autoremove',
]

COMMAND_DESC = [
    ('install', 'Install external commands'),
    ('purge', 'Uninstall commandt'),
    ('update', 'Update the fetch lists'),
    ('upgrade', 'Upgrade currently installed commands'),
    ('autoremove', 'Remove data that belonged to other commands'),
]


class Command(CommandInterface):
    def init(self):

        self.parser = Parser(prog="fpm", description="(Flux Package Manager)  Package manager similar to apt to install additional commands.", add_help=True)
        self.parser.add_argument("command", nargs="?", help="The command to execute")
        self.parser.add_argument("-l", dest="list", action="store_true",  help="List available commands")
    
    def run(self):
        self.args = self.parser.parse_args(self.command[1:])

        if self.parser.exit_execution:
            print()
            return
        
        if self.args.list:
            from src.utils.format import create_adaptive_table
            self.stdout.write(create_adaptive_table("Name", "Description", contents=COMMAND_DESC))
