from components.arduino import Arduino


class Stepper:
    arduino: Arduino
    current_percentage: int
    is_bouncing: bool

    def __init__(self, arduino: Arduino):
        self.arduino = arduino
        self.current_percentage = 0
        self.is_bouncing = False

    def move(self, percentage: int, velocity: int, bounce_distance: int, bounce_velocity: int):
        self.current_percentage = percentage
        self.arduino.move_stepper(self.current_percentage, velocity, bounce_distance, bounce_velocity)
