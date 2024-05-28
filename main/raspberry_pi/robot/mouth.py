from components.arduino import Arduino
from components.curve import Curve
from components.servo import Servo
from components.speaker import Speaker
from robot.side import Side
from robot.sounds import Sounds


class Mouth:
    bottom_servo: Servo
    top_servo: Servo
    voice: Speaker
    open_angle_top: int
    closed_angle_top: int
    open_angle_bottom: int
    closed_angle_bottom: int

    def __init__(self, side: Side, arduino: Arduino, top_index: int, bottom_index: int, open_angle_top: int,
                 closed_angle_top: int, open_angle_bottom: int, closed_angle_bottom: int, volume: int):
        self.bottom_servo = Servo(arduino, bottom_index)
        self.top_servo = Servo(arduino, top_index)
        self.voice = Speaker(side, volume)
        self.open_angle_top = open_angle_top
        self.closed_angle_top = closed_angle_top
        self.open_angle_bottom = open_angle_bottom
        self.closed_angle_bottom = closed_angle_bottom

    def open_percent(self, percent: int, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        assert 0 <= percent <= 100
        assert 0 <= delay
        assert 0 <= velocity
        self.top_servo.add_movement(int(self.closed_angle_top + (self.open_angle_top - self.closed_angle_top) * (percent / 100)),
                                    velocity, delay, curve)
        self.bottom_servo.add_movement(int(self.closed_angle_bottom + (self.open_angle_bottom - self.closed_angle_bottom) * (percent / 100)),
                                       velocity, delay, curve)

    def close(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.open_percent(0, velocity, delay, curve)

    def open(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.open_percent(100, velocity, delay, curve)

    def open_half(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.open_percent(50, velocity, delay, curve)

    def ñamñam(self, times: int, velocity: int, curve: Curve = Curve.LINEAR, delay_between: int = 0):
        for _ in range(times):
            self.open(velocity, delay_between, curve)
            self.close(velocity, delay_between, curve)

    def say(self, sound: Sounds):
        self.voice.play(sound.value)
        
    def say_and_wait(self, sound: Sounds):
        self.voice.play_and_wait(sound.value)
