from typing import List, Optional
from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

import os
import shutil


class Command(CommandInterface):
    def init(self):
        self.parser = Parser(
            prog="chown",
            description="Change the owner and/or group of each FILE to OWNER and/or GROUP"
        )
        self.parser.add_argument("owner", help="the new owner (can be [OWNER] or [OWNER]:[GROUP])")
        self.parser.add_argument("file", nargs="+", help="the file(s) to modify")

    def run(self):
        # windows does not support shutil.chown
        if not hasattr(os, "chown") or os.name == 'nt':
            self.error("chown is not supported on this platform (Windows).", use_color=True)
            return

        for f in self.args.file:
            if not os.path.exists(f):
                self.error(self.errors.file_not_found(f))

        # Parse owner[:group]
        parts: List[str] = [i for i in self.args.owner.split(":") if i]
        if len(parts) == 0 or len(parts) > 2:
            self.error("invalid owner format (expected OWNER or OWNER:GROUP)")
            return

        owner: Optional[str] = parts[0] if len(parts) >= 1 else None
        group: Optional[str] = parts[1] if len(parts) == 2 else None

        for file in self.args.file:
            try:
                shutil.chown(file, user=owner, group=group)
            except LookupError as e:
                # User or group not found
                self.error(str(e))
            except PermissionError:
                self.error(f"permission denied: cannot change ownership of '{file}'")
            except Exception as e:
                self.error(str(e))
