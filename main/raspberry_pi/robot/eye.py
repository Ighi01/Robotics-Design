from digitalio import DigitalInOut

from components.screen import Screen
from components.stepper import Stepper
from components.arduino import Arduino
from robot.side import Side


class Eye:
    side: Side
    stepper: Stepper
    max_velocity: int
    screen: Screen

    def __init__(self, side: Side, arduino: Arduino, max_velocity: int, cs: DigitalInOut, dc: DigitalInOut, rst: DigitalInOut):
        self.side = side
        self.stepper = Stepper(arduino)
        self.max_velocity = max_velocity
        self.screen = Screen(cs, dc, rst)
        
    def raise_percent(self, percent: int, velocity_percent: int, bounce_distance: int = 0, bounce_velocity_percentage: int = 0):
        self.stepper.move(percent, int(velocity_percent / 100 * self.max_velocity), bounce_distance, bounce_velocity_percentage / 100 * self.max_velocity)

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
        self.screen.gif(f'static/eyes/sad-{self.side.value}.gif')
