from typing import Any
from adafruit_hcsr04 import HCSR04


class ProximitySensor:
    trigger_pin: Any
    echo_pin: Any
    device: HCSR04

    def __init__(self, trigger_pin: Any, echo_pin: Any):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.device = HCSR04(trigger_pin, echo_pin)

    @property
    def distance(self):
        return self.device.distance