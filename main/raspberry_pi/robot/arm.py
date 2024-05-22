from components.arduino import Arduino
from components.servo import Servo
from components.curve import Curve


class Arm:
    servo: Servo
    max_velocity: int
    max_angle: int
    min_angle: int

    def __init__(self, arduino: Arduino, max_velocity: int, index: int, max_angle: int, min_angle: int = 0):
        self.servo = Servo(arduino, index)
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.max_velocity = max_velocity

    def raise_percent(self, percent: int, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        assert 0 <= percent <= 100
        assert 0 <= delay
        assert 0 <= velocity <= self.max_velocity
        self.servo.add_movement(int(self.max_angle * percent / 100), delay, velocity, curve)

    def raise_full(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.raise_percent(100, delay, velocity, curve)

    def lower(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.raise_percent(0, delay, velocity, curve)

    def raise_half(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.raise_percent(50, delay, velocity, curve)
