from digitalio import DigitalInOut

from components.screen import Screen
from robot.side import Side


class Eye:
    side: Side
    screen: Screen

    def __init__(self, side: Side, cs: DigitalInOut, dc: DigitalInOut, rst: DigitalInOut):
        self.screen = Screen(cs, dc, rst)

    def blank(self):
        self.screen.blank()

    def angry_1(self):
        self.screen.gif(f'static/eyes/angry1-{self.side.value}.gif')

    def angry_2(self):
        self.screen.gif(f'static/eyes/angry2-{self.side.value}.gif')

    def comp(self):
        self.screen.gif(f'static/eyes/comp-{self.side.value}.gif')

    def happy_1(self):
        self.screen.gif(f'static/eyes/happy1-{self.side.value}.gif')

    def happy_2(self):
        self.screen.gif(f'static/eyes/happy2-{self.side.value}.gif')

    def neutral(self):
        self.screen.gif(f'static/eyes/neutral-{self.side.value}.gif')

    def sad(self):
        self.screen.gif(f'static/eyes/sad1-{self.side.value}.gif')
