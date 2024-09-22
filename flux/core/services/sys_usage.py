import os
import psutil
import time

from flux.core.helpers.services import ServiceInterface
from flux.core.system.interrupts import EventTriggers

class Service(ServiceInterface):

    def awake(self) -> None:
        self.metadata["description"] =  "monitor how much CPU and RAM is Flux using and warn for excessive usage"

        self.pid = os.getpid()
                
        # process wide usage
        self.threshold_cpu = .9
        self.threshold_ram = .9

        self.above_threshold = False

    def update(self) -> None:
        try:
            if self.get_cpu_usage() > self.threshold_cpu:
                if not self.above_threshold:
                    # in the future this will also be logged
                    self.system.interrupt_handler.raise_interrupt(EventTriggers.CPU_USAGE_HIGH)
                    self.above_threshold = True
            
            elif self.get_ram_usage() > self.threshold_ram:
                if not self.above_threshold:
                    # in the future this will also be logged
                    self.system.interrupt_handler.raise_interrupt(EventTriggers.MEMORY_USAGE_HIGH)
                    self.above_threshold = True
            else:
                self.above_threshold = False
        except:
            pass

    def get_ram_usage(self):
        try:
            process = psutil.Process(self.pid)
            return process.memory_percent()
        except psutil.NoSuchProcess:
            # kinda difficult to reach here
            return 0

    def get_cpu_usage(self):
        try:
            process = psutil.Process(self.pid)
            return process.cpu_percent()
        except psutil.NoSuchProcess:
            # kinda difficult to reach here
            return 0