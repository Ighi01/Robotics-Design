from components.arduino import Arduino


class Servo:
    arduino: Arduino
    index: int

    def __init__(self, arduino: Arduino, index: int):
        self.arduino = arduino
        self.index = index

    def add_movement(self, angle: int, delay: int, velocity: int):
        self.arduino.add_servo_movement(self.index, angle, delay, velocity)
