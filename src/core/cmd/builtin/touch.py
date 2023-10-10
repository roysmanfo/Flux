"""
# `touch`
Update the access and modification times of each FILE to the current time.

A FILE argument that does not exist is created empty, unless -c or -h
is supplied.
"""

from ...helpers.commands import *
from ...helpers.arguments import Parser
import os
import time

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="touch", add_help=True, description="Update the access and modification times of each FILE to the current time. Or create an empty one")
        self.parser.add_argument("FILE", help='the file to modify/create')
        self.parser.add_argument('-a', action='store_true', help='change only the access time')
        self.parser.add_argument('-c', '--no-create', action='store_true', help='do not create any files')
        self.parser.add_argument('-m', action='store_true', help='change only the modification time')

    def run(self):
        self.logger.path = self.args.FILE

        if not os.path.exists(self.args.FILE):
            if not self.args.no_create:
                try:
                    with open(self.args.FILE, "w") as f:
                        f.write("")
                    return True
                
                except PermissionError:
                    self.error(STATUS_ERR, self.logger.permission_denied())
                    return
            else:
                self.error(STATUS_ERR, self.logger.path_not_found())
                return


        if not self.args.m:
            self.modify_access_info()

        if not self.args.a:
            self.modify_modification_time()


    def modify_access_info(self):
        try:
            os.utime(self.args.FILE, (time.time(), os.stat(self.args.FILE).st_mtime))
            return True
        
        except PermissionError:
            self.error(STATUS_ERR, self.logger.permission_denied())
            return False
        
        except FileNotFoundError:
            self.error(STATUS_ERR, self.logger.path_not_found())
            return False         

    def modify_modification_time(self):
        try:
            os.utime(self.args.FILE, (os.stat(self.args.FILE).st_atime, time.time()))
            return True
        except PermissionError:
            self.error(STATUS_ERR, self.logger.permission_denied())
            return False