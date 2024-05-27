import logging
from typing import Any
from adafruit_hcsr04 import HCSR04


log = logging.getLogger(__name__)


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
        distances = []
        i = 3
        while i:
            try:
                distances.append(self.device.distance)
                i -= 1
            except Exception as _:
                log.debug('Timeout on proximity sensor, trying again...')
        return sum(distances) / len(distances)
