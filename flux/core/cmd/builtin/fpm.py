from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)
from flux.utils.tables import create_table
from pathlib import Path
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
    
    ### flux api methods ###

    def init(self):

        self.parser = Parser(prog="fpm", description="(Flux Package Manager)  Package manager similar to apt to install additional commands.")
        self.parser.usage = "fpm command [options]"
        self.parser.add_argument("command", nargs="?", help="The command to execute")
        self.parser.add_argument("-l", dest="list", action="store_true",  help="List available commands")


        self.db_path: Path = self.settings.syspaths.LOCAL_FOLDER.value / "fpm" / "state.db"
        self.db: sqlite3.Connection = None
    
    def setup(self):
        if len(self.line_args) == 1:
            self.line_args.append("-h")
        super().setup()
    
    def run(self):
        
        if self.args.list:
            self.print(create_table("Name", "Description", rows=COMMAND_DESC))
        else:
            match self.args.command:
                case "list":
                    self.cmd_list()
                
                case _: self.error(f"unknown command '{self.args.command}'")


    ### custom methods ###
    
    def _init_connection(func):
        """
        Decorator to initialize the database connection before executing a function.
        """
        def wrapper(self, *args, **kwargs):
            self.init_db()
            if self.db is None:
                self.db = sqlite3.connect(self.db_path)
            return func(self, *args, **kwargs)
        return wrapper

    def init_db(self):
        if not self.db_path.exists():
            self._create_db()
        


    def _create_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path.write_bytes(b"")

        with sqlite3.connect(self.db_path) as db:
            db.execute("""
                CREATE TABLE command_types(
                    name TEXT PRIMARY KEY
                )
            """)

            # may change the id to TEXT and use a uuid instead of a number
            db.execute("""
                CREATE TABLE commands(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    install_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    version TEXT,
                    description TEXT,
                    type TEXT NOT NULL,
                       
                    FOREIGN KEY (type) REFERENCES command_types(name)
                )
            """)

            db.commit()
        


            self.print(create_table("name", "description", rows=COMMAND_DESC))


    def init_db(self):
        if not self.db_path.exists():
            self._create_db()
        
    @_init_connection
    def cmd_list(self):
        
        # this print will not be redirected to another file
        print("Listing commands...", end="\r" if not self.redirected_stdout else "\n")
        
        with self.db:
            cursor = self.db.cursor()
            cursor.execute("SELECT id, name, version FROM commands")
            rows = cursor.fetchall()
            if rows:
                self.print(create_table("id", "name", "version", rows=rows))
            else:
                self.print("No commands installed.")

        


