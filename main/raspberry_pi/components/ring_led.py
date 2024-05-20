from typing import Any
from neopixel import NeoPixel


class RingLED:
    pin: Any
    device: NeoPixel

    def __init__(self, pin: Any, num_leds: int = 12):
        self.pin = pin
        self.device = NeoPixel(pin, num_leds)
