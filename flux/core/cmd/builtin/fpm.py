from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

import sqlite3

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


        self.db_path = self.settings.syspaths.LOCAL_FOLDER.value / "fpm" / "state.db"
        self.db: sqlite3.Connection = None
    
    def setup(self):
        if len(self.line_args) == 1:
            self.line_args.append("-h")
        super().setup()
    
    def run(self):
        
        if self.args.list:
            from flux.utils.format import create_table
            self.print(create_table("Name", "Description", rows=COMMAND_DESC))


    def init_db(self):
        if not self.db_path.exists():
            self._create_db()
        


    def _create_db(self):
        self.db_path.parent.mkdir(parents=True)
        self.db_path.write_bytes(b"")

        with sqlite3.connect(self.db_path) as db:
            db.execute("""
                CREATE TABLE command_types(
                    name TEXT PRIMARY KEY
                )
            """)
        
            db.execute("""
                CREATE TABLE commands(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    install_date DATE NOT NULL,
                    version TEXT,
                    type TEXT,
                       
                    FOREIGN KEY (type) REFERENCES command_types(name)
                )
            """)

            db.commit()
        


