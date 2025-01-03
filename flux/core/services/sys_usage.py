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
        # process wide usage
        self.threshold_battery = .2
        self.f_battery_sig_sent = False 

        self.above_threshold = False
        self.cooldown = 1


    def update(self) -> None:
        try:
            # cpu usage
            if self.get_cpu_usage() > self.threshold_cpu:
                if not self.above_threshold:
                    # in the future this will also be logged
                    self.system.interrupt_handler.raise_interrupt(EventTriggers.CPU_USAGE_HIGH)
                    self.above_threshold = True
            
            # ram usage
            elif self.get_ram_usage() > self.threshold_ram:
                if not self.above_threshold:
                    # in the future this will also be logged
                    self.system.interrupt_handler.raise_interrupt(EventTriggers.MEMORY_USAGE_HIGH)
                    self.above_threshold = True
            else:
                self.above_threshold = False

            # battery percentage
            if self.get_battery_percentage() < self.threshold_battery:
                if not self.f_battery_sig_sent:
                    # in the future this will also be logged
                    self.system.interrupt_handler.raise_interrupt(EventTriggers.BATTERY_LOW)
                    self.f_battery_sig_sent = True
            else:
                self.f_battery_sig_sent = False
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
        
    def get_battery_percentage(self):
        if (battery := psutil.sensors_battery()):
            if battery.power_plugged:
                return battery.percent / 100
        
        # if there is no battery or the battery is full,
        # act like there is a full battery
        return 1
