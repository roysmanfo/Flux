from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)

import os
import curses

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="less", description="View FILE contents one screen at a time")
        self.parser.add_argument("FILE", nargs='?', help="the file to view")

    def run(self):
        file = self.args.FILE
        lines: list[str] = []

        if file:
            if not os.path.exists(file):
                self.error(self.errors.file_not_found(file))
                return

            try:
                with open(file, "r") as f:
                    lines = f.readlines()
            except Exception as e:
                self.error(str(e))
                return

        elif self.recv_from_pipe:
            lines = self.stdin.readlines()
        
        else:
            self.error('Missing filename')
            return
             


        def pager(stdscr: curses.window):
            curses.curs_set(0)  # hide cursor
            height, width = stdscr.getmaxyx()
            pos = 0

            while True:
                stdscr.clear()
                for i in range(height - 1):
                    if pos + i < len(lines):
                        stdscr.addstr(i, 0, lines[pos + i][:width - 1])
                stdscr.addstr(height - 1, 0, "-- Press q to quit, ↑/↓ to scroll --")

                key = stdscr.getch()
                if key in (ord("q"), 27):  # q or ESC
                    break
                elif key in (curses.KEY_DOWN, ord("j")) and pos < len(lines) - 1:
                    pos += 1
                elif key in (curses.KEY_UP, ord("k")) and pos > 0:
                    pos -= 1
                elif key in (curses.KEY_NPAGE,):  # Page down
                    pos = min(pos + height - 1, len(lines) - 1)
                elif key in (curses.KEY_PPAGE,):  # Page up
                    pos = max(pos - (height - 1), 0)

        curses.wrapper(pager)

