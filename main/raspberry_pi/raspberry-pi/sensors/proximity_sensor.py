from adafruit_hcsr04 import HCSR04
from board import Pin


class ProximitySensor:
    trigger_pin: Pin
    echo_pin: Pin
    device: HCSR04

    def __init__(self, trigger_pin: Pin, echo_pin: Pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.device = HCSR04(trigger_pin, echo_pin)

    @property
    def distance(self):
        return self.device.distance