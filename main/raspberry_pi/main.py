#!/home/dietpi/.cache/pypoetry/virtualenvs/raspberry-pi-SQ1rTMlp-py3.11/bin/python

from time import sleep
import board
import pygame
from digitalio import DigitalInOut
import RPi.GPIO as GPIO
from components.curve import Curve


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
    
    robot.left.eye.neutral()
    robot.right.eye.neutral()
    
    #1    
    robot.left.mouth.open(30,0,Curve.QUADRATIC)
    robot.left.arm.raise_percent(90,72,0,Curve.CUBIC)
    robot.left.neck.look_away(30,0,Curve.QUADRATIC)
    robot.left.neck.look_down(15,0)
    
    robot.right.mouth.open(21,2,Curve.QUADRATIC)
    robot.right.arm.raise_percent(90,57,2,Curve.CUBIC)
    robot.right.neck.look_away(30,2,Curve.QUADRATIC)
    robot.right.neck.look_down(11,2)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    
    #2
    robot.left.mouth.close(30,0,Curve.QUADRATIC)
    robot.left.mouth.open(30,1,Curve.QUADRATIC)
    robot.left.arm.raise_half(64,1,Curve.BOUNCE)
    robot.left.arm.raise_percent(90,64,2,Curve.CUBIC)
    robot.left.neck.look_up(15,1)
    robot.left.neck.look_down(15,2)
    
    robot.right.mouth.close(21,2,Curve.QUADRATIC)
    robot.right.mouth.open(21,1,Curve.QUADRATIC)
    robot.right.arm.raise_half(64,3,Curve.BOUNCE)
    robot.right.arm.raise_percent(90,64,4,Curve.CUBIC)
    robot.right.neck.look_up(15,3)
    robot.right.neck.look_down(15,4)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    
    #3
    robot.left.mouth.close(30,0,Curve.QUADRATIC)
    robot.left.mouth.open(30,1,Curve.QUADRATIC)
    robot.left.arm.raise_half(64,1,Curve.BOUNCE)
    robot.left.arm.raise_percent(90,64,2,Curve.CUBIC)
    robot.left.neck.look_up(15,1)
    robot.left.neck.look_down(15,2)
    
    robot.right.mouth.close(21,2,Curve.QUADRATIC)
    robot.right.mouth.open(21,1,Curve.QUADRATIC)
    robot.right.arm.raise_half(64,3,Curve.BOUNCE)
    robot.right.arm.raise_percent(90,64,4,Curve.CUBIC)
    robot.right.neck.look_up(15,3)
    robot.right.neck.look_down(15,4)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    
    #4
    robot.left.mouth.close(30,0,Curve.QUADRATIC)
    robot.left.mouth.open(30,1,Curve.QUADRATIC)
    robot.left.arm.raise_half(64,1,Curve.BOUNCE)
    robot.left.arm.raise_percent(90,64,2,Curve.CUBIC)
    robot.left.neck.look_up(15,1)
    robot.left.neck.look_down(15,2)
    
    robot.right.mouth.open(21,2,Curve.QUADRATIC)
    robot.right.mouth.close(21,1,Curve.QUADRATIC)
    robot.right.arm.raise_half(64,3,Curve.BOUNCE)
    robot.right.arm.raise_percent(90,64,4,Curve.CUBIC)
    robot.right.neck.look_up(15,3)
    robot.right.neck.look_down(15,4)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)


if __name__ == '__main__':
    main()
    GPIO.cleanup()
