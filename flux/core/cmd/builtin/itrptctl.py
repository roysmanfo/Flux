from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)
from flux.utils.format import create_table


class Command(CommandInterface):
    def init(self):
        description = "Interrupt Controller, allows to gather information on currently registered " \
                      "interrupts, both running and dormant ones"
        self.parser = Parser('itrptctl', description=description)

    def run(self):
        
        self.list_interrupts()
    
    def list_interrupts(self):
        # signals = self.system.interrupt_handler.get_supported_signals()
        interrupt_data: list[tuple[int, str]] = [] # handle -> interrupt info
        
        for handle in self.system.interrupt_handler.interrupt_map:
            interrupt = self.system.interrupt_handler.find(handle)
            interrupt.signal
            
            interrupt_data.append((
                int(handle),
                self.system.interrupt_handler.event_value_to_name(interrupt.signal),
                interrupt.signal,
                interrupt.exec_count,
                interrupt.exec_once,
            ))
        if interrupt_data:
            table = create_table('handle', 'event_name', 'event_value', 'exec_count', 'exec_once', rows=interrupt_data)
            self.print(table)
        else:
            self.warning('no interrupts registered yet')
