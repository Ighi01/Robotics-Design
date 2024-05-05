from .arduino import Arduino


class Stepper:
    arduino: Arduino
    index: int

    def __init__(self, arduino: Arduino, index: int):
        self.arduino = arduino
        self.index = index

    def move(self, percentage: int, velocity: int, bouncing_length: int, bouncing_velocity: int):
        command = f"2 {self.index} {percentage} {velocity} {bouncing_length} {bouncing_velocity}"
        self.arduino.write(command)
