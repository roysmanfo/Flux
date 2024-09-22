from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)


COMMANDS_AVAILABLE = [
    'autoremove',
    'install',
    'list',
    'purge',
    'search',
    'update',
    'upgrade',
]

COMMAND_DESC = [
    ('autoremove', 'Remove data that belonged to other commands'),
    ('install', 'Install external commands'),
    ('list', 'List packages based on package names'),
    ('search', 'Search in package descriptions'),
    ('purge', 'Uninstall commands'),
    ('update', 'Update the fetch lists'),
    ('upgrade', 'Upgrade currently installed commands'),
]


class Command(CommandInterface):
    def init(self):

        self.parser = Parser(prog="fpm", description="(Flux Package Manager)  Package manager similar to apt to install additional commands.")
        self.parser.usage = "fpm [options] command"
        self.parser.add_argument("command", nargs="?", help="The command to execute")
        self.parser.add_argument("-l", dest="list", action="store_true",  help="List available commands")
    
    def setup(self):
        if len(self.line_args) == 1:
            self.line_args.append("-h")
        super().setup()
    
    def run(self):
        
        if self.args.list:
            from flux.utils.format import create_table
            self.print(create_table("Name", "Description", contents=COMMAND_DESC))
