#!/home/dietpi/.cache/pypoetry/virtualenvs/raspberry-pi-SQ1rTMlp-py3.11/bin/python

from time import sleep
import board
import pygame
from digitalio import DigitalInOut
import RPi.GPIO as GPIO


try:
    pygame.mixer.init()
except pygame.error:
    print('Error connecting to audio device.')

GPIO.setmode(GPIO.BCM)

from robot.robot import Robot
from robot.side import Side
from robot.sounds import Sounds


def main():
    robot = Robot(
        left={
            'side': Side.LEFT,
            'arduino_port': '/dev/ARL',
            'eye': {
                'cs': DigitalInOut(board.D17),
                'rst': DigitalInOut(board.D24),
                'dc': DigitalInOut(board.D25),
                'max_velocity': 33,
            },
            'arm': {
                'index': 4,
                'min_angle': 80,
                'max_angle': 0,
                'max_velocity': 200,
            },
            'mouth': {
                'top_index': 0,
                'bottom_index': 1,
                'open_angle_top': 0,
                'closed_angle_top': 40,
                'open_angle_bottom': 0,
                'closed_angle_bottom': 40,
                'audio_channel_index': 1,
            },
            'neck': {
                'horizontal_index': 3,
                'vertical_index': 2,
                'max_angle_vertical': 20,
                'min_angle_vertical': 50,
                'center_angle_vertical': 35,
                'max_angle_horizontal': 180,
                'min_angle_horizontal': 0,
                'center_angle_horizontal': 30,
                'ir_sensor_pin': 19,
            },
        },
        right={
            'side': Side.RIGHT,
            'arduino_port': '/dev/ARR',
            'eye': {
                'cs': DigitalInOut(board.D27),
                'rst': DigitalInOut(board.D5),
                'dc': DigitalInOut(board.D6),
                'max_velocity': 33,
            },
            'arm': {
                'index': 4,
                'min_angle': 0,
                'max_angle': 75,
                'max_velocity': 200,
            },
            'mouth': {
                'top_index': 0,
                'bottom_index': 1,
                'open_angle_top': 30,
                'closed_angle_top': 0,
                'open_angle_bottom': 30,
                'closed_angle_bottom': 0,
                'audio_channel_index': 1,
            },
            'neck': {
                'horizontal_index': 3,
                'vertical_index': 2,
                'max_angle_vertical': 65,
                'min_angle_vertical': 35,
                'center_angle_vertical': 50,
                'max_angle_horizontal': 0,
                'min_angle_horizontal': 180,
                'center_angle_horizontal': 150,
                'ir_sensor_pin': 16,
            },
        },
        proximity_sensor={
            'trigger_pin': board.D20,
            'echo_pin': board.D21,
        },
    )
    robot.left.arduino.connect()
    robot.right.arduino.connect()
    
    robot.left.mouth.open(4,)
    robot.left.mouth.ñamñam(4,)
    robot.left.neck.look_to_other(400)
    robot.right.neck.look_to_other(400)
    
    robot.send_servo_movements()


if __name__ == '__main__':
    main()
    GPIO.cleanup()
