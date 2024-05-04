import threading

import digitalio
from ..arduino.serial_communication import SerialCommunication
from ..arduino.servo import Servo
from ..arduino.stepper import Stepper
# from ..audio.audio_player import AudioPlayer
from ..screen.screen import Screen
from ..sensors.ir_sensor import IRSensor
from ..sensors.proximity_sensor import ProximitySensor

from .engaging import Engaging
from .feedback import Feedback
from .voting import Voting


class StateMachine:
    def __init__(self, ir_sensor1_pin, ir_sensor2_pin, proximity_trigger_pin, proximity_echo_pin, left_screen_pins,
                 right_screen_pins, servo_controller_serial, stepper_controller_serial, audio_pin):

        self.states = {
            'engaging': Engaging(self),
            'voting': Voting(self),
            'feedback': Feedback(self)
        }

        # INITIAL STATE
        self.current_state = 'engaging'

        # FIRST IR SENSOR
        self.ir_sensor1 = IRSensor(ir_sensor1_pin, self)

        # SECOND IR SENSOR
        self.ir_sensor2 = IRSensor(ir_sensor2_pin, self)

        # PROXIMITY SENSOR
        self.proximity_sensor = ProximitySensor(proximity_trigger_pin, proximity_echo_pin)
        self.proximity_thread = threading.Thread(target=self.proximity_sensor.measure_distance_task)
        self.proximity_thread.start()

        # AUDIO
        # self.audio_player = AudioPlayer(audio_pin)

        # SCREENS
        self.left_screen = Screen(digitalio.DigitalInOut(left_screen_pins[0]),
                                  digitalio.DigitalInOut(left_screen_pins[1]),
                                  digitalio.DigitalInOut(left_screen_pins[2]))
        self.right_screen = Screen(digitalio.DigitalInOut(right_screen_pins[0]),
                                   digitalio.DigitalInOut(right_screen_pins[1]),
                                   digitalio.DigitalInOut(right_screen_pins[2]))

        # SERVOMOTORS
        self.arduino_0 = SerialCommunication(servo_controller_serial)
        self.servos = [Servo(self.arduino_0, i) for i in range(12)]

        # STEPPER MOTOR
        self.arduino_1 = SerialCommunication(stepper_controller_serial)
        self.steppers = [Stepper(self.arduino_1, i) for i in range(3)]

    def moveMultipleServo(self, servo_movements):
        for servo, movements in servo_movements.items():
            self.servos[servo].move(*movements)

    def moveMultipleStepper(self, stepper_movements):
        for stepper, movement in stepper_movements.items():
            self.steppers[stepper].move(*movement)

    def checkAllServoCompleted(self, *indexes):
        for index in indexes:
            if not self.servos[index].is_completed():
                return False
        return True

    def run(self):
        while True:
            state_function = self.states[self.current_state].run
            state_function()
