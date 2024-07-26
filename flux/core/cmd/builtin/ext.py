import os
import subprocess
from flux.core.helpers.commands import (
    CommandInterface,
    Parser,
    Status
)


p: subprocess.Popen = None


class Command(CommandInterface):

    def init(self):
        self.parser = Parser(
            "ext", description="Allows to use commands from outside flux")
        self.parser.add_argument(
            "command", action="append", help="the command to run")

    def setup(self):
        if "-h" in self.line_args and self.line_args.index("-h") == 1:
            super().setup()

        elif "--help" in self.line_args and self.line_args.index("--help") == 1:
            super().setup()

        elif len(self.line_args) < 2:
            # print an help message
            self.line_args.append("-h")
            super().setup()

        elif len(self.line_args[1:]) == 0:
            self.error(self.errors.parameter_not_specified("command"))
            self.parser.exit_execution = True
            return

        self.line_args = self.line_args[1:]

    def run(self):
        global p

        try:
            # find the executable
            process = subprocess.Popen(['where' if os.name == 'nt' else "which",self.line_args[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            self.status = Status.STATUS_ERR

    def close(self):
        if not self.status:
            self.status = p.returncode if p else Status.STATUS_ERR
