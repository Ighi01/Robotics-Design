from components.arduino import Arduino
from components.curve import Curve
from components.servo import Servo
from components.speaker import Speaker
from robot.side import Side


class Mouth:
    bottom_servo: Servo
    top_servo: Servo
    voice: Speaker
    open_angle_top: int
    closed_angle_top: int
    open_angle_bottom: int
    closed_angle_bottom: int

    def __init__(self, side: Side, arduino: Arduino, top_index: int, bottom_index: int, open_angle_top: int,
                 closed_angle_top: int, open_angle_bottom: int, closed_angle_bottom: int, audio_channel_index: int):
        self.bottom_servo = Servo(arduino, bottom_index)
        self.top_servo = Servo(arduino, top_index)
        self.voice = Speaker(audio_channel_index, side)
        self.open_angle_top = open_angle_top
        self.closed_angle_top = closed_angle_top
        self.open_angle_bottom = open_angle_bottom
        self.closed_angle_bottom = closed_angle_bottom

    def open_percent(self, percent: int, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        assert 0 <= percent <= 100
        assert 0 <= delay
        assert 0 <= velocity
        self.top_servo.add_movement(percent * (self.open_angle_top - self.closed_angle_top) / 100 + self.closed_angle_top,
                                    velocity, curve, delay)
        self.bottom_servo.add_movement(percent * (self.open_angle_bottom - self.closed_angle_bottom) / 100 + self.closed_angle_bottom,
                                       velocity, curve, delay)

    def close(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.open_percent(0, delay, velocity, curve)

    def open(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.open_percent(100, delay, velocity, curve)

    def open_half(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.open_percent(50, delay, velocity, curve)

    def ñamñam(self, times: int, velocity: int, curve: Curve = Curve.LINEAR, delay_between: int = 0):
        for _ in range(times):
            self.open(delay_between, velocity, curve)
            self.close(delay_between, velocity, curve)
