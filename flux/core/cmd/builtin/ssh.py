from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)

import paramiko
import socket
import getpass
import time

class Command(CommandInterface):
    def init(self):
        self.parser = Parser("ssh", usage="usage: ssh [options] [user@]host [command]", description="OpenSSH remote login client")
        self.parser.add_argument("host", nargs="?", help="the host to connect to")
        self.parser.add_argument("-p", dest="port", type=int, default=22, help="port to connect to on the remote host")

    def setup(self):
        if len(self.line_args) == 1:
            self.line_args.append("-h")
        super().setup()


    def run(self):
        host = username = ""

        if "@" not in self.args.host:
            host = self.args.host
            username = self.system.settings.user.username
        elif self.args.host.count("@") == 1:
            username, host = self.args.host.split("@")
        else:
            *username, host = self.args.host.split("@")
            username = "@".join(username)

        _, _, ip_addresses = socket.gethostbyname_ex(host)
        
        if not ip_addresses:
            self.print(f"ssh: Could not resolve hostname {host}: Name or service not known")
            return


        self.connect(username, host)
    


    def connect(self, username: str, host: str) -> None:
        try:
            with paramiko.SSHClient() as ssh:
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                passw = None
                key = None

                for i in range(3):
                    if not ssh.get_host_keys().lookup(host):
                        self.print(f"Host key for {host} not found. Proceeding with password authentication.")
                        passw = getpass.getpass(f"{username}@{host}'s password: ")

                    try:
                        ssh.connect(
                            hostname=host,
                            port=self.args.port,
                            password=passw,
                            username=username,
                            pkey=key,
                        )
                        break
                    except paramiko.AuthenticationException:
                        if i == 2:
                            self.print(f"{username}@{host}: Permission denied (publickey,password).")
                            return
                        self.print("Permission denied, please try again.")
                    except Exception as e:
                        self.print(f"Error connecting to {host}: {e}")
                        return

                shell_exit = False
                with ssh.invoke_shell() as shell:
                    # Receive the welcome message
                    time.sleep(0.1)
                    while shell.recv_ready():
                        out = shell.recv(1024).decode()
                        self.print(out, end="")
                    self.print()

                    while not shell_exit:
                        try:
                            command = input()
                            if command.strip().lower() == "exit":
                                shell_exit = True
                                continue

                            # Send command
                            shell.send(command + "\n")
                            time.sleep(0.2)

                            # Receive command output
                            first_line_received = False
                            while shell.recv_ready():
                                out = shell.recv(1024).decode()

                                # the first line is the command itself,
                                # so we don't want to print it
                                if not first_line_received:
                                    out = out.split("\n", 1)[1]
                                self.print(out, end="")

                            # Check for errors
                            while shell.recv_stderr_ready():
                                err = shell.recv_stderr(1024).decode()
                                self.print(err, end="")

                        except Exception as e:
                            self.print(f"Error during shell session: {e}")
                            shell_exit = True

                self.print(f"Connection to {host} closed.")
        except Exception as e:
            self.print(f"An error occurred: {e}")


