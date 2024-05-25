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
