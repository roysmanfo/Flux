import os
import subprocess
from flux.core.helpers.commands import *
from flux.core.helpers.arguments import Parser



p: subprocess.Popen = None
class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser("ext", description="Allows to use commands from outside flux")
        self.parser.add_argument("command", action="append", help="the command to run")

    def setup(self):
        if "-h" in self.command and self.command.index("-h") == 1:
            super().setup()
        
        elif "--help" in self.command and self.command.index("--help") == 1:
            super().setup()
        
        elif len(self.command) < 2:
            # print an help message
            self.command.append("-h")
            super().setup()

        elif len(self.command[1:]) == 0 :
            self.error(self.errors.parameter_not_specified("command"))
            self.parser.exit_execution = True
            return

        self.command = self.command[1:]

    def run(self):
        global p


        try:
            # find the executable
            if os.name == 'nt':
                process = subprocess.Popen(['where', self.command[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(['which', self.command[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            stdout, _ = process.communicate()


            if process.returncode == 0:
                command_paths = [i.strip() for i in stdout.decode().strip().split('\n') if i]

                success = False
                # try each path
                for path in command_paths:
                    try:
                        p = subprocess.Popen([path])
                        p.wait()
                        success = True
                    except:
                        pass

                if not success:
                    raise FileNotFoundError()


            else:
               raise FileNotFoundError()

        except FileNotFoundError:
            self.error("unable to spawn the specified process (not found)")
            self.status = STATUS_ERR

    def close(self):
        if not self.status:
            self.status = p.returncode if p else STATUS_ERR

