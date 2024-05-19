from components.arduino import Arduino
from components.servo import Servo


class Arm:
    servo: Servo
    max_velocity: int
    max_angle: int
    min_angle: int

    def __init__(self, arduino: Arduino, max_velocity: int, index: int, max_angle: int, min_angle: int = 0):
        self.servo = Servo(arduino, index)
        self.max_angle = max_angle
        self.min_angle = min_angle

    def raise_percent(self, percent: int, delay: int, velocity: int):
        assert 0 <= percent <= 100
        assert 0 <= delay
        assert 0 <= velocity <= self.max_velocity
        self.servo.add_movement(int(self.max_angle * percent / 100), delay, velocity)

    def raise_full(self, delay: int, velocity: int):
        self.raise_percent(100, delay, velocity)

    def lower(self, delay: int, velocity: int):
        self.raise_percent(0, delay, velocity)

    def raise_half(self, delay: int, velocity: int):
        self.raise_percent(50, delay, velocity)
