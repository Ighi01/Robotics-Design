import board

from state_machine.state_machine import StateMachine

# Pin Definitions
IR_SENSOR1_PIN = 4
IR_SENSOR2_PIN = 19
PROXIMITY_TRIGGER_PIN = board.D20
PROXIMITY_ECHO_PIN = board.D21
AUDIO_PIN = board.D22
LEFT_SCREEN_PINS = (board.D17, board.D25, board.D24)
RIGHT_SCREEN_PINS = (board.D27, board.D6, board.D5)
SERVO_CONTROLLER = '/dev/ttyUSB0'
STEPPER_CONTROLLER = '/dev/ttyUSB1'


def main():
    state_machine = StateMachine(IR_SENSOR1_PIN, IR_SENSOR2_PIN, PROXIMITY_TRIGGER_PIN, PROXIMITY_ECHO_PIN,
                                 LEFT_SCREEN_PINS, RIGHT_SCREEN_PINS, SERVO_CONTROLLER, STEPPER_CONTROLLER, AUDIO_PIN)
    state_machine.run()


if __name__ == '__main__':
    main()
