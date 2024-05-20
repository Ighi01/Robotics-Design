from components.arduino import Arduino
from components.servo import Servo
from components.speaker import Speaker
from components.curve import Curve
from robot.side import Side


class Mouth:
    bottom_servo: Servo
    top_servo: Servo
    voice: Speaker
    max_angle_top: int
    max_angle_bottom: int

    def __init__(self, side: Side, arduino: Arduino, top_index: int, top_max_angle: int, bottom_index: int, bottom_max_angle: int,
                 audio_channel_index: int):
        self.bottom_servo = Servo(arduino, bottom_index)
        self.top_servo = Servo(arduino, top_index)
        self.voice = Speaker(audio_channel_index, side)
        self.max_angle_top = top_max_angle
        self.max_angle_bottom = bottom_max_angle

    def open_percent(self, percent: int, delay: int, velocity: int, curve: Curve = Curve.LINEAR):
        self.bottom_servo.add_movement(int(self.max_angle_bottom * percent / 100), delay, velocity, curve)
        self.top_servo.add_movement(int(self.max_angle_top * percent / 100), delay, velocity, curve)

    def close(self, delay: int, velocity: int, curve: Curve = Curve.LINEAR):
        self.open_percent(0, delay, velocity, curve)

    def open(self, delay: int, velocity: int, curve: Curve = Curve.LINEAR):
        self.open_percent(100, delay, velocity, curve)

    def open_half(self, delay: int, velocity: int, curve: Curve = Curve.LINEAR):
        self.open_percent(50, delay, velocity, curve)

    def ñamñam(self, times: int, velocity: int, curve: Curve = Curve.LINEAR, delay_between: int = 0):
        for _ in range(times):
            self.open(delay_between, velocity, curve)
            self.close(delay_between, velocity, curve)
