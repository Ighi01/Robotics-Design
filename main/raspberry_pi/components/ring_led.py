from board import Pin
from neopixel import NeoPixel


class RingLED:
    pin: Pin
    device: NeoPixel

    def __init__(self, pin: Pin, num_leds: int = 12):
        self.pin = pin
        self.device = NeoPixel(pin, num_leds)
