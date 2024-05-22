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

    def __init__(self, arduino: Arduino, horizontal_index: int, vertical_index: int, ir_sensor_pin: int):
        self.stepper = Stepper(arduino)
        self.horizontal_servo = Servo(arduino, horizontal_index)
        self.vertical_servo = Servo(arduino, vertical_index)
        #self.sensor = IRSensor(ir_sensor_pin)

    def turn_head_horizontal(self, angle: int, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.horizontal_servo.add_movement(angle, delay, velocity, curve)

    def turn_head_vertical(self, angle: int, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.vertical_servo.add_movement(angle, delay, velocity, curve)

    def look_front(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_horizontal(self.center_angle_horizontal, velocity, delay, curve)

    def look_to_other(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_horizontal(self.max_angle_horizontal, velocity, delay, curve)

    def look_away(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_horizontal(self.min_angle_horizontal, velocity, delay, curve)

    def look_up(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_vertical(0, velocity, delay, curve)

    def look_down(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_vertical(180, velocity, delay, curve)

    def look_center(self, velocity: int, delay: int = 0, curve: Curve = Curve.LINEAR):
        self.turn_head_vertical(self.center_angle_vertical, velocity, delay, curve)
