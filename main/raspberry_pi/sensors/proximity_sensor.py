from adafruit_hcsr04 import HCSR04
from board import Pin
import threading
import time

class ProximitySensor:
    trigger_pin: Pin
    echo_pin: Pin
    device: HCSR04
    machine: StateMachine
    nextState: bool

    def __init__(self, trigger_pin: Pin, echo_pin: Pin, machine: StateMachine):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.device = HCSR04(trigger_pin, echo_pin)
        self.distance_thread = threading.Thread(target=self.distance_checker)
        self.distance_thread.daemon = True
        self.distance_thread.start()
        self.nextState = False
        self.machine = machine

    @property
    def distance(self):       #non credo che serva
        return self.device.distance

    def distance_checker(self):
        while True:            
            if self.machine.getstate().id == 'Engaging' and distance < 100:
                self.nextState = True
            if self.getstate().id == 'Voting' and distance > 250:
                self.nextState = True
            time.sleep(0.1)