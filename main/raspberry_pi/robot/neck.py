from components.arduino import Arduino
from components.curve import Curve
from components.ir_sensor import IRSensor
from components.servo import Servo
from components.stepper import Stepper


class Neck:
    stepper: Stepper
    horizontal_servo: Servo
    vertical_servo: Servo
    sensor: IRSensor
    max_angle_vertical: int
    min_angle_vertical: int
    center_angle_vertical: int
    max_angle_horizontal: int
    min_angle_horizontal: int
    center_angle_horizontal: int

    def __init__(self, arduino: Arduino, horizontal_index: int, vertical_index: int, 
                 max_angle_vertical: int, 
                 min_angle_vertical: int,
                 center_angle_vertical: int,
                 max_angle_horizontal: int,
                 min_angle_horizontal: int,
                 center_angle_horizontal: int,
                 ir_sensor_pin: int):
        self.stepper = Stepper(arduino)
        self.horizontal_servo = Servo(arduino, horizontal_index)
        self.vertical_servo = Servo(arduino, vertical_index)
        self.max_angle_vertical = max_angle_vertical
        self.min_angle_vertical = min_angle_vertical
        self.center_angle_vertical = center_angle_vertical
        self.max_angle_horizontal = max_angle_horizontal
        self.min_angle_horizontal = min_angle_horizontal
        self.center_angle_horizontal = center_angle_horizontal
        self.sensor = IRSensor(ir_sensor_pin)

    def turn_head_horizontal(self, angle: int, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.horizontal_servo.add_movement(angle, velocity, delay, curve)

    def turn_head_vertical(self, angle: int, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.vertical_servo.add_movement(angle, velocity, delay, curve)

    def look_front(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        """
        On the horizontal index
        """
        self.turn_head_horizontal(self.center_angle_horizontal, velocity, delay, curve)

    def look_to_other(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_horizontal(self.max_angle_horizontal, velocity, delay, curve)

    def look_away(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_horizontal(self.min_angle_horizontal, velocity, delay, curve)

    def look_up(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_vertical(self.max_angle_vertical, velocity, delay, curve)

    def look_down(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_vertical(self.min_angle_vertical, velocity, delay, curve)

    def look_center(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        """
        On the vertical index
        """
        self.turn_head_vertical(self.center_angle_vertical, velocity, delay, curve)
