from components.proximity_sensor import ProximitySensor
from components.ring_led import RingLED
from robot.robot_side import RobotSide


class Robot:
    left_side: RobotSide
    right_side: RobotSide
    proximity_sensor: ProximitySensor
    ring_leds: RingLED

    def __init__(self, left_side: dict, right_side: dict, proximity_sensor: dict, ring_leds: dict):
        self.left_side = RobotSide(**left_side)
        self.right_side = RobotSide(**right_side)
        self.proximity_sensor = ProximitySensor(**proximity_sensor)
        self.ring_leds = RingLED(**ring_leds)
