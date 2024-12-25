from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

import paramiko
import socket
import getpass


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

        names, _, ip_addresses = socket.gethostbyname_ex(host)
        
        print(names)
        if not ip_addresses:
            self.print(f"ssh: Could not resolve hostname {host}: Name or service not known")
            return


        self.print(f"Connecting to {host} as {username}")
        self.connect(username, host)
    
    def connect(self, username: str, host: str) -> None:
        with paramiko.SSHClient() as ssh:
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            passw = None
            if not (key := ssh.get_host_keys().lookup(host)):
                # todo: handle key error
                passw = getpass.getpass(f"{username}@{host}'s password: ")

            ssh.connect(
                hostname=host,
                port=self.args.port,
                password=passw,
                username=username,
                pkey=key
            )
            
            exit_status = 0
            prompt = f"{self.colors.Fore.GREEN}{self.colors.Style.BRIGHT}{username}@{host}{self.colors.Style.NORMAL}{self.colors.Fore.RESET}"
            path = "~"
            input_prompt_separator = f"{self.colors.Style.BRIGHT}${self.colors.Style.NORMAL}"
            
            while not exit_status:
                command = input(f"{prompt}:{self.colors.Fore.BLUE}{path} {input_prompt_separator}{self.colors.Fore.RESET} ")
                if command == "exit":
                    break
                _, stdout, stderr = ssh.exec_command(command)

                if out := stdout.read():
                    self.print(out.decode())
                
                if err := stderr.read():
                    self.print(err.decode())
                
                exit_status = stdout.channel.recv_exit_status()


