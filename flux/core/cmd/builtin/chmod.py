from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)

import os
import stat
import re


class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="chmod", description="Change the mode of each FILE to MODE")
        self.parser.add_argument("mode", help="the new file mode (e.g., 755, u+x, g-w, a+rw)")
        self.parser.add_argument("FILE", nargs="+", help="the file(s) to modify")

    def run(self):
        for f in self.args.FILE:
            if not os.path.exists(f):
                self.error(self.errors.file_not_found(f))

        mode_str = self.args.mode
        self.check_windows_chmod_support(mode_str)

        for file in self.args.FILE:
            try:
                if mode_str.isdigit():
                    # Numeric mode like "755"
                    mode = int(mode_str, 8)
                else:
                    # Symbolic mode like u+x, g-w
                    mode = self.apply_symbolic_mode(file, mode_str)

                os.chmod(file, mode)

            except Exception as e:
                self.error(str(e))

    def apply_symbolic_mode(self, file: str, mode_str: str) -> int:
        """
        Apply symbolic chmod (like u+x, g-w) to a file.
        Returns the new numeric mode.
        """
        current_mode = os.stat(file).st_mode
        current_perms = stat.S_IMODE(current_mode)

        # Regex: [ugoa]* [+-=] [rwxXst]+
        pattern = r"([ugoa]*)([+-=])([rwxXst]+)"
        matches = re.finditer(pattern, mode_str)

        for match in matches:
            who, op, perms = match.groups()

            if not who:
                who = "a"

            perm_bits = 0
            for p in perms:
                if p == "r":
                    perm_bits |= stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
                elif p == "w":
                    perm_bits |= stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
                elif p == "x":
                    perm_bits |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                elif p == "X":  # only if directory or any exec already set
                    if os.path.isdir(file) or (current_perms & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)):
                        perm_bits |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                elif p == "s":  # setuid/setgid
                    perm_bits |= stat.S_ISUID | stat.S_ISGID
                elif p == "t":  # sticky bit
                    perm_bits |= stat.S_ISVTX

            for target in who:
                if target == "u":
                    mask = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_ISUID)
                elif target == "g":
                    mask = (stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_ISGID)
                elif target == "o":
                    mask = (stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)
                elif target == "a":
                    mask = (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO | stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX)

                if op == "+":
                    current_perms |= (perm_bits & mask)
                elif op == "-":
                    current_perms &= ~(perm_bits & mask)
                elif op == "=":
                    current_perms &= ~mask
                    current_perms |= (perm_bits & mask)

        return current_perms

    def check_windows_chmod_support(self, mode_str: str):
        """
        On Windows, os.chmod only respects the read-only flag (S_IREAD / S_IWRITE).
        All other bits (x, g/o perms, s, t) are ignored.
        This function warns the user if they try unsupported flags.
        """
        if os.name != "nt":
            return  # Only check on Windows

        unsupported = []

        # Numeric modes: only 400 (read) and 200 (write) bits have meaning
        if mode_str.isdigit():
            try:
                mode_val = int(mode_str, 8)
                # Check if execute bits are set
                if mode_val & 0o111:
                    unsupported.append("execute (x)")
                # Check if group/other perms are set
                if mode_val & 0o770:
                    unsupported.append("group/other permissions")
                # Check for special bits
                if mode_val & 0o7000:
                    unsupported.append("setuid/setgid/sticky")
            except ValueError:
                pass  # invalid numeric mode will be caught elsewhere

        else:  # Symbolic mode
            if any(c in mode_str for c in ["x", "X"]):
                unsupported.append("execute (x)")
            if any(c in mode_str for c in ["g", "o", "a"]):
                unsupported.append("group/other permissions")
            if any(c in mode_str for c in ["s", "t"]):
                unsupported.append("setuid/setgid/sticky")

        if unsupported:
            self.warning(f"Windows ignores: {', '.join(set(unsupported))}", use_color=True, to_stdout=False)
