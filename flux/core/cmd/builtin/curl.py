from flux.core.helpers.commands import *
import urllib.request
import requests



class Command(CommandInterface):
    def init(self):
        self.parser = Parser("curl", description=" transfer a URL", usage="curl [options...] <url>")
        self.parser.add_argument("url", nargs="?")
    
    def run(self):
        print(self.args.url)

