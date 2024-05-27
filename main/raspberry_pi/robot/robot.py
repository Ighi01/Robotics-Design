from components.proximity_sensor import ProximitySensor
from robot.robot_side import RobotSide


class Robot:
    left: RobotSide
    right: RobotSide
    proximity_sensor: ProximitySensor

    def __init__(self, left: dict, right: dict, proximity_sensor: dict):
        self.left = RobotSide(**left)
        self.right = RobotSide(**right)
        self.proximity_sensor = ProximitySensor(**proximity_sensor)

    def connect_arduinos(self):
        self.left.arduino.connect()
        self.right.arduino.connect()

    def send_servo_movements(self):
        self.left.arduino.send_servo_movements()
        self.right.arduino.send_servo_movements()
        
    def reset(self, left_servos: list = [], right_servos: list = []):
        self.left.arduino.reset(left_servos)
        self.right.arduino.reset(right_servos)
        
    def close(self):
        self.left.arm.raise_full(150)
        self.right.arm.raise_full(150)
        self.send_servo_movements()
        self.left.eye.raise_percent(0, 100)
        self.right.eye.raise_percent(0, 100)
        