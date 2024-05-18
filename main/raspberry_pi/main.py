import board

from robot.robot import Robot
from robot.side import Side


def main():
    robot = Robot(
        left_side={
            'side': Side.LEFT,
            'arduino_port': '/dev/ttyUSB0',
            'eye': {
                'cs': board.D17,
                'dc': board.D25,
                'rst': board.D24,
            },
            'arm': {
                'index': 0,
            },
            'mouth': {
                'top_index': 1,
                'top_max_angle': 90,
                'bottom_index': 2,
                'bottom_max_angle': 90,
                'audio_channel_index': 0,
            },
            'neck': {
                'horizontal_index': 3,
                'vertical_index': 4,
                'ir_sensor_pin': 4,
            },
        },
        right_side={
            'side': Side.RIGHT,
            'arduino_port': '/dev/ttyUSB1',
            'eye': {
                'cs': board.D27,
                'dc': board.D6,
                'rst': board.D5,
            },
            'arm': {
                'index': 0,
                'max_angle': 80,
                'max_velocity': 200,
            },
            'mouth': {
                'top_index': 1,
                'top_max_angle': 20,
                'bottom_index': 2,
                'bottom_max_angle': 20,
                'audio_channel_index': 1,
            },
            'neck': {
                'horizontal_index': 3,
                'vertical_index': 4,
                'ir_sensor_pin': 19,
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
