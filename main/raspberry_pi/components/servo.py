from components.arduino import Arduino
from components.curve import Curve


class Servo:
    arduino: Arduino
    index: int

    def __init__(self, arduino: Arduino, index: int):
        self.arduino = arduino
        self.index = index

    def add_movement(self, angle: int, delay: int, velocity: int, curve: Curve):
        self.arduino.add_servo_movement(self.index, angle, delay, velocity, curve)
        
    def is_finished(self):
        return self.arduino.is_finished([self.index])

    def reset(self):
        self.arduino.reset([self.index])