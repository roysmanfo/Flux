from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)

ENTRY_POINT = 'Hex'
DEFAULT_COLS = 76

class Hex(CommandInterface):
    def init(self):
        self.parser = Parser('hex', description='Hex-encodes data provided on the command line or stdin')
        self.parser.add_argument("data", nargs='*', help='data to convert to hex')
        self.parser.add_argument('-p', '--prefix', default='', help='insert a prefix before each byte')
        self.parser.add_argument('-s', '--separator', default='', help='add a separator between each byte')


    def run(self):
        if not (data := self.read_input()):
            return
        
        hex_data = data.hex(sep=' ', bytes_per_sep=1).split()
        hex_data = str(self.args.separator).join(f'{self.args.prefix}{i}' for i in hex_data)
        self.print(hex_data)
        
    def read_input(self) -> bytes | None:
        data = ' '.join(self.args.data) if self.args.data else None
        if data:
            return data.encode()

        content = inp = ''
        while (inp := self.input()) is not None:
            content += inp
        return content.encode()
