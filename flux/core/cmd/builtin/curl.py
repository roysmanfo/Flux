from flux.core.helpers.commands import *

import requests


SUPPORTED_SCHEMAS = {"http", "https"}

class Command(CommandInterface):
    def init(self):
        self.parser = Parser("curl", description=" transfer a URL", usage="curl [options...] <url>")
        self.parser.add_argument("url", help="the page to visit")
        self.parser.add_argument("-A", "--user-agent", dest="agent", default="curl", help="Send User-Agent <name> to server")
        self.parser.add_argument("-H", "--header", action="append", dest="header", help="Extra header to include in information sent")
        self.parser.add_argument("-v", "--verbose", action="store_true", help="Make the operation more talkative")

        self.log_level = self.levels.INFO

    def run(self):

        if self.args.verbose:
            self.log_level = self.levels.DEBUG


        url: str = self.args.url

        if not "://" in url:
            url = "http://" + url

        if not url[:url.index("://")] in SUPPORTED_SCHEMAS:
            self.error("unsupported schema")
            return

        headers = self.format_headers()

        try:
            res = requests.get(
                url=url,
                headers=headers,
                allow_redirects=False
            )

            self.print(res.status_code, res.reason)
            self.print(res.text)
        except requests.exceptions.ConnectionError as e:
            self.fatal(f"(7) Failed to connect to {self.args.url}: Connection refused")


    def format_headers(self) -> dict[str, str]:
        headers = {"User-Agent": self.args.agent}        
        for h in self.args.header:
            try:
                sep = h.index(":")
                headers.update({h[:sep].strip() : h[sep+1:].strip()})

            except ValueError:
                pass # ignore this header

        return headers