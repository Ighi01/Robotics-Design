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

    def __init__(self, arduino: Arduino, horizontal_index: int, vertical_index: int, ir_sensor_pin: int):
        self.stepper = Stepper(arduino)
        self.horizontal_servo = Servo(arduino, horizontal_index)
        self.vertical_servo = Servo(arduino, vertical_index)
        #self.sensor = IRSensor(ir_sensor_pin)

    def turn_head_horizontal(self, angle: int, delay: int, velocity: int, curve: Curve = Curve.LINEAR):
        self.horizontal_servo.add_movement(angle, delay, velocity, curve)

    def turn_head_vertical(self, angle: int, delay: int, velocity: int, curve: Curve = Curve.LINEAR):
        self.vertical_servo.add_movement(angle, delay, velocity, curve)
