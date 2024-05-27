from components.proximity_sensor import ProximitySensor
from robot.robot_side import RobotSide

import pygame


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
        
    def start_eyes(self):
        self.left.eye.screen.start()
        self.right.eye.screen.start()
        
    def stop_eyes(self):
        self.left.eye.screen.stop()
        self.right.eye.screen.stop()
        
    def start_voice(self):
        pygame.mixer.init(channels=2)
        self.left.mouth.voice.start(0)
        self.right.mouth.voice.start(1)

    def send_servo_movements(self):
        self.left.arduino.send_servo_movements()
        self.right.arduino.send_servo_movements()
        
    def set_ir_callbacks(self, left_callback: callable, right_callback: callable):
        self.left.neck.sensor.set_callback(left_callback)
        self.right.neck.sensor.set_callback(right_callback)
        
    def remove_ir_callbacks(self):
        self.left.neck.sensor.remove_callback()
        self.right.neck.sensor.remove_callback()
    