from flux.core.helpers.commands import *

import requests


class Command(CommandInterface):
    def init(self):
        self.parser = Parser("curl", description=" transfer a URL", usage="curl [options...] <url>")
        self.parser.add_argument("url", help="the page to visit")
        self.parser.add_argument("-A", "--user-agent", dest="agent", default="curl", help="Send User-Agent <name> to server")

        self.log_level = self.levels.INFO

    def run(self):
        res = requests.get(
            url=self.args.url,
            headers={"User-Agent": self.args.agent},
        )

        self.print(res.status_code, res.reason)
        self.print(res.content)
