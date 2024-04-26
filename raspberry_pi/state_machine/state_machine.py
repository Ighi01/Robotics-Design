from state_machine.engaging import Engaging
from state_machine.voting import Voting
from state_machine.feedback import Feedback
from screen.screen import Screen
from arduino.serial_communication import SerialCommunication
from arduino.servo import Servo
from arduino.stepper import Stepper
from sensors.ir_sensor import IRSensor
from sensors.proximity_sensor import ProximitySensor
import digitalio
import threading
import time

class StateMachine:
    def __init__(self, ir_sensor1_pin, ir_sensor2_pin, proximity_trigger_pin, proximity_echo_pin, left_screen_pins, right_screen_pins, servo_controller, stepper_controller):

        self.states = {
            'engaging': Engaging(self),
            'voting': Voting(self),
            'feedback': Feedback(self)
        }

        # INITIAL STATE
        self.current_state = 'engaging'

        # FIRST IR SENSOR
        self.ir_sensor1 = IRSensor(ir_sensor1_pin)

        # SECOND IR SENSOR
        self.ir_sensor2 = IRSensor(ir_sensor2_pin)

        # PROXIMITY SENSOR
        self.proximity_sensor = ProximitySensor(proximity_trigger_pin, proximity_echo_pin)
        self.proximity_thread = threading.Thread(target=self.proximity_sensor.measure_distance_task)
        self.proximity_thread.start()

        # SCREENS
        self.left_screen = Screen(digitalio.DigitalInOut(left_screen_pins[0]), digitalio.DigitalInOut(left_screen_pins[1]), digitalio.DigitalInOut(left_screen_pins[2]))
        self.right_screen = Screen(digitalio.DigitalInOut(right_screen_pins[0]), digitalio.DigitalInOut(right_screen_pins[1]), digitalio.DigitalInOut(right_screen_pins[2]))
    
        # SERVOMOTORS
        self.arduino_0 = Arduino(servo_controller)
        self.servo_0 = Servo(self.arduino_0, 0)
        self.servo_1 = Servo(self.arduino_0, 1)
        self.servo_2 = Servo(self.arduino_0, 2)
        self.servo_3 = Servo(self.arduino_0, 3)

        # STEPPER MOTOR
        self.arduino_1 = Arduino(stepper_controller)
        # TODO: Inizializzare stepper1
        # TODO: Inizializzare stepper2

        # SOUND
        # TODO: Inizializzare il modulo per i suoni

    def run(self):
        while True:
            state_function = self.states[self.current_state].run
            state_function()
