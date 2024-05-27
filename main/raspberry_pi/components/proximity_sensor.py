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
        return 100
        distances = []
        while i := 3:
            try:
                distances.append(self.device.distance)
                i -= 1
            except Exception as _:
                print('Timeout on proximity sensor, trying again...')
        return sum(distances) / len(distances)
