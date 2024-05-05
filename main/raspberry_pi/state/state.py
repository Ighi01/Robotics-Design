from board import Pin
from digitalio import DigitalInOut
from statemachine import StateMachine, State

from arduino.arduino import Arduino
from arduino.servo import Servo
from arduino.servo_arduino import ServoArduino
from arduino.stepper import Stepper
from arduino.stepper_arduino import StepperArduino
from screen.screen import Screen
from sensors.ir_sensor import IRSensor
from sensors.proximity_sensor import ProximitySensor

import random


class SM(StateMachine):
    """
    This class is a state machine that represents the different states of the voting process.
    Documentation on the order in which the callbacks are called can be found in
    https://python-statemachine.readthedocs.io/en/latest/actions.html#ordering
    """

    #################
    #  Definitions  #
    #################
    # These are the devices attached to the robot (and thus to the state machine)
    ir_sensor_left: IRSensor
    ir_sensor_right: IRSensor
    proximity_sensor: ProximitySensor

    screen_left: Screen
    screen_right: Screen

    servo_arduino: ServoArduino
    stepper_arduino: StepperArduino

    servo_right_shoulder: Servo
    servo_right_elbow: Servo
    servo_right_wrist: Servo
    servo_left_shoulder: Servo
    servo_left_elbow: Servo
    servo_left_wrist: Servo
    servo_right_neck: Servo
    servo_left_neck: Servo
    servo_right_mouth_upper: Servo
    servo_right_mouth_lower: Servo
    servo_left_mouth_upper: Servo
    servo_left_mouth_lower: Servo

    stepper_right: Stepper
    stepper_left: Stepper

    # These are the states of the state machine
    engaging = State('Engaging', initial=True)
    voting = State('Voting')
    feedback = State('Feedback')
    # TODO: Maybe a fourth state for the final result?

    # These are the transitions of the state machine
    loopEngaging = engaging.to.itself()
    approached = engaging.to(voting)
    leaved = voting.to(engaging)
    voted_engaging = engaging.to(feedback) 
    voted = voting.to(feedback) 
    feedbacked = feedback.to(engaging)

    # This is the constructor of the state machine
    def __init__(self, ir_sensor_right_pin: int, ir_sensor_left_pin: int, proximity_trigger_pin: Pin,
                 proximity_echo_pin: Pin,
                 screen_left_pins: tuple, screen_right_pins: tuple,
                 serial_communication_servos_port: str, serial_communication_steppers_port: str):
        super(SM, self).__init__()

        self.ir_sensor_right = IRSensor(ir_sensor_right_pin, self)
        self.ir_sensor_left = IRSensor(ir_sensor_left_pin, self)

        self.proximity_sensor = ProximitySensor(proximity_trigger_pin, proximity_echo_pin)

        self.screen_left = Screen(*screen_left_pins)
        self.screen_right = Screen(*screen_right_pins)

        self.servo_arduino = ServoArduino(serial_communication_servos_port)
        self.stepper_arduino = StepperArduino(serial_communication_steppers_port)

        self.servo_right_shoulder = Servo(self.servo_arduino, 0)
        self.servo_right_elbow = Servo(self.servo_arduino, 1)
        self.servo_right_wrist = Servo(self.servo_arduino, 2)
        self.servo_left_shoulder = Servo(self.servo_arduino, 3)
        self.servo_left_elbow = Servo(self.servo_arduino, 4)
        self.servo_left_wrist = Servo(self.servo_arduino, 5)
        self.servo_right_neck = Servo(self.servo_arduino, 6)
        self.servo_left_neck = Servo(self.servo_arduino, 7)
        self.servo_right_mouth_upper = Servo(self.servo_arduino, 8)
        self.servo_right_mouth_lower = Servo(self.servo_arduino, 9)
        self.servo_left_mouth_upper = Servo(self.servo_arduino, 10)
        self.servo_left_mouth_lower = Servo(self.servo_arduino, 11)

        self.stepper_right = Stepper(self.stepper_arduino, 0)
        self.stepper_left = Stepper(self.stepper_arduino, 1)

    #######################
    #  General callbacks  #
    #######################
    # These are the callbacks that are called on every transition

    def before_transition(self, to_state, *args, **kwargs):
        pass

    def on_exit_state(self, state, *args, **kwargs):
        pass

    def on_transition(self, from_state, to_state, *args, **kwargs):
        pass

    def on_enter_state(self, state, *args, **kwargs):
        pass

    def after_transition(self, state, *args, **kwargs):
        pass

    #######################
    #   State callbacks   #
    #######################
    # These are the callbacks that are called on specific states

    def on_enter_engaging(self):
        pass

    def on_exit_engaging(self):
        pass
    
    

    def on_enter_voting(self):
        pass

    def on_exit_voting(self):
        pass
    
    
    

    def on_enter_feedback(self):
        pass

    def on_exit_feedback(self):
        pass

    ##########################
    #  Transition callbacks  #
    ##########################
    # These are the callbacks that are called on specific transitions

    def before_approached(self):
        pass

    def on_approached(self):
        pass

    def after_approached(self):
        pass
    
    

    def before_voted(self):
        pass

    def on_leaved(self):
        if self.ir_sensor_right.counter == 0 and self.ir_sensor_right.counter == 0:
            stepper_movements = {
                0: [50, 100, 3, 200],
                1: [50, 100, 3, 200]
            }
        self.moveMultipleStepper(stepper_movements) #TODO BETTER
            
        random_index = random.randint(0, len(self.routines) - 1)
        while self.current_routine_index == random_index:
            random_index = random.randint(0, len(self.routines) - 1)
        self.current_routine_index = random_index
        self.fsm.moveMultipleServo(self.routines[self.current_routine_index])
                

        pass

    def on_feedbacked(self):
        self.on_leaved()
        pass

            
        
            
            
