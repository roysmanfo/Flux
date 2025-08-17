import os
import hashlib
from flux.core.helpers.commands import (
    CommandInterface,
    Parser,
    PreLoadConfigs
)


class Command(CommandInterface):

    PRELOAD_CONFIGS = PreLoadConfigs(prefered_mode_stdin='b')

    def init(self):
        self.parser = Parser(prog="sha256sum", description="Print or check SHA256 (256-bit) checksums")
        self.parser.add_argument("FILE", nargs="*", help="With no FILE, or when FILE is -, read standard input.")
        self.parser.add_argument("-c", "--check", action="store_true", help="read SHA256 sums from the FILE(s) and check them")
        self.parser.add_argument("--tag", action="store_true", help="create a BSD-style checksum")
        self.parser.add_argument("--ignore-missing", action="store_true", help="don't fail or report status for missing files")
        self.parser.add_argument("--quiet", action="store_true", help="don't print OK for each successfully verified file")
        self.parser.add_argument("--status", action="store_true", help="don't output anything, status code shows success")

    def run(self):
        files: list[str] = self.args.FILE
        
        if not files:
            files = ["-"]

        if self.args.quiet:
            self.log_level = self.levels.WARNING

        if self.args.status:
            self.log_level = self.levels.ERROR

        report_missing = not self.args.ignore_missing

        if self.args.check:
            # check mode: treat FILES as checksum files
            for checksum_file in files:
                if not os.path.exists(checksum_file) and report_missing:
                    self.error(self.errors.file_not_found(checksum_file))
                    continue

                with open(checksum_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue

                        try:
                            expected_hash, filename = line.split(None, 1)
                            filename = filename.strip()
                        except ValueError:
                            self.error(f"skipping malformed line in {checksum_file!r}: {line!r}")
                            continue

                        if not os.path.exists(filename) and report_missing:
                            self.error(self.errors.file_not_found(filename))
                            continue

                        actual_hash = self._hash_file(filename)
                        if actual_hash == expected_hash:
                            self.info(f"{filename}: OK") # suppressed with --quiet/--status
                        else:
                            self.warning(f"{filename}: FAILED") # suppressed with --status

        else:
            # normal mode: compute and print checksums
            for file_path in files:
                if file_path == "-":
                    sha256 = hashlib.sha256()
                    while (_in := self.input(n=4096)):
                        sha256.update(_in)

                    if self.args.tag:
                        self.print(f"SHA256 (-) = {sha256.hexdigest()}")
                    else:                    
                        self.print(f"{sha256.hexdigest()}  -")
                else:
                    if not os.path.exists(file_path) and report_missing:
                        self.error(self.errors.file_not_found(file_path))
                        continue

                    digest = self._hash_file(file_path)
                    if self.args.tag:
                        self.print(f"SHA256 ({file_path}) = {digest}")
                    else:                    
                        self.print(f"{digest}  {file_path}")


    def _hash_file(self, path: str) -> str:
        """Compute SHA256 hash of a file in binary mode."""
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def close(self):
        self.print() # add a newline at the end
        return super().close()
