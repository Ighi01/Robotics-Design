from components.proximity_sensor import ProximitySensor
from components.ring_led import RingLED
from robot.robot_side import RobotSide


class Robot:
    left: RobotSide
    right: RobotSide
    proximity_sensor: ProximitySensor
    ring_leds: RingLED

    def __init__(self, left: dict, right: dict, proximity_sensor: dict, ring_leds: dict):
        #self.left = RobotSide(**left)
        self.right = RobotSide(**right)
        self.proximity_sensor = ProximitySensor(**proximity_sensor)
        self.ring_leds = RingLED(**ring_leds)
