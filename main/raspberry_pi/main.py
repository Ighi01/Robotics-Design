from time import sleep
import board
import pygame

from robot.robot import Robot
from robot.side import Side


def main():
    try:
        pygame.mixer.init()
    except pygame.error:
        print('Error connecting to audio device. Exiting...')
        return
    robot = Robot(
        left={
            'side': Side.LEFT,
            'arduino_port': '/dev/ARL',
            'eye': {
                'cs': board.D17,
                'rst': board.D24,
                'dc': board.D25,
            },
            'arm': {
                'index': 4,
                'max_angle': 75,
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
                'horizontal_index': 2,
                'vertical_index': 3,
                'max_angle_vertical': 45,
                'min_angle_vertical': 25,
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
                'cs': board.D27,
                'rst': board.D5,
                'dc': board.D6,
            },
            'arm': {
                'index': 4,
                'max_angle': 75,
                'max_velocity': 200,
            },
            'mouth': {
                'top_index': 0,
                'bottom_index': 1,
                'open_angle_top': 20,
                'closed_angle_top': 0,
                'open_angle_bottom': 20,
                'closed_angle_bottom': 0,
                'audio_channel_index': 1,
            },
            'neck': {
                'horizontal_index': 2,
                'vertical_index': 3,
                'max_angle_vertical': 0,
                'min_angle_vertical': 0,
                'center_angle_vertical': 0,
                'max_angle_horizontal': 0,
                'min_angle_horizontal': 0,
                'center_angle_horizontal': 0,
                'ir_sensor_pin': 16,
            },
        },
        proximity_sensor={
            'trigger_pin': board.D20,
            'echo_pin': board.D21,
        },
        ring_leds={
            'pin': board.D10,
        }
    )


if __name__ == '__main__':
    main()
