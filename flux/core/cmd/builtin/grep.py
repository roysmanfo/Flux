from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

import re
from io import TextIOWrapper
from typing import Generator, TextIO, Union


class Command(CommandInterface):
    def init(self):
        self.parser = Parser("grep", description="Search for PATTERNS in each FILE.")
        self.parser.add_argument("pattern", metavar="PATTERNS", help="the pattern to search for")
        self.parser.add_argument("files", metavar="FILE", nargs="*", help="the file(s) to search into")

        patterns_arggroup = self.parser.add_argument_group(title="Pattern selection and interpretation:")
        patterns_arggroup.add_argument("-i", "--ignore-case", action="store_true", help="ignore case distinctions in patterns and data")

    def run(self):
        if self.args.ignore_case:
            self.args.pattern = self.args.pattern.lower()

        if self.recv_from_pipe:
            self.args.files.append(self.stdin)
        
        for file in self.args.files:
            if isinstance(file, str):
                try:
                    file = open(file, "rt")
                except FileNotFoundError:
                    self.error(self.errors.file_not_found(file))
                    continue

            for line in self.search_pattern_in_file(file, mark_matches=True):
                self.print(line)


    def search_pattern_in_file(self, file: Union[TextIO, TextIOWrapper], mark_matches: bool) -> Generator[str, None, None]:
        while line := file.readline().strip().strip('\n'):
            compared_line = line.lower() if self.args.ignore_case else line
            matches = list(re.compile(self.args.pattern).finditer(compared_line))
            if matches:
                if mark_matches:
                    for match in matches[::-1]:
                        start, end = match.span()
                        line = line[:start] + self.colors.Fore.RED + line[start:end] + self.colors.Fore.RESET + line[end:]

                yield line

