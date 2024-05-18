from digitalio import DigitalInOut

from components.screen import Screen


class Eye:
    screen: Screen

    def __init__(self, cs: DigitalInOut, dc: DigitalInOut, rst: DigitalInOut):
        self.screen = Screen(cs, dc, rst)

