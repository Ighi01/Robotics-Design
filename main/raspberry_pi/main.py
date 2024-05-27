#!/home/dietpi/.cache/pypoetry/virtualenvs/raspberry-pi-SQ1rTMlp-py3.11/bin/python

from time import sleep
import board
from digitalio import DigitalInOut
import RPi.GPIO as GPIO
import logging
from rich.logging import RichHandler

GPIO.setmode(GPIO.BCM)

logging.basicConfig(
    level="DEBUG",
    format='%(message)s',
    datefmt='[%Y-%m-%d %X]',
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            locals_max_length=30,
        )
    ],
)
log = logging.getLogger(__name__)


def main():
    from robot.robot import Robot
    from robot.side import Side
    from robot.sounds import Sounds
    from components.curve import Curve
    from state.state import SM
    from state.routines import engaging_1, engaging_2, engaging_3, voting, feedback_left_1, feedback_left_2, feedback_left_3, feedback_right_1, feedback_right_2, feedback_right_3
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
                'volume': 20,
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
                'volume': 20,
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
    state_machine = SM(robot)


if __name__ == '__main__':
    main()
