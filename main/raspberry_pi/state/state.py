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
    setup = State('setup', initial=True)
    engaging = State('Engaging')
    voting = State('Voting')
    feedback = State('Feedback')

    # These are the transitions of the state machine
    setup_ready = setup.to(engaging)
    loopEngaging = engaging.to.itself()
    loopVoting = voting.to.itself()
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
    #   State callbacks   #
    #######################

    def on_enter_setup(self):
        while !self.servo_arduino.read():
            time.sleep(1)
            continue
        self.servo_arduino.write("ack");

        while !self.stepper_arduino.read():
            time.sleep(1)
            continue
        self.stepper_arduino.write("ack");
        self.setup_ready()

    def on_enter_engaging(self): #TODO
        # if command2
            # move steppers depending on counters
            # move servos (command 1) drawing from one avaible routine or depending on emotion posssibly different from a previous one
            # show screen (or more than one) depending on emotion (?)
            # play audio (or more than one) depending on emotion (?)
        if self.proximity_sensor.nextState:
            self.proximity_sensor.nextState = False
            self.approached()
            return
        if self.ir_sensor_right.nextState or self.ir_sensor_left.nextState:
            self.ir_sensor_right.nextState = False
            self.ir_sensor_right.nextState = False
            self.voted_engaging()
            return
        self.loopEngaging()
    
    def on_enter_feedback(self): #TODO
        # move steppers (maybe not here)
        # move servos (command 1) depending on the vote
        # show screen (or more than one) depending on the vote
        # play audio (or more than one) depending on the vote
        self.feedbacked()

    def on_enter_voting(self): 
        time.sleep(1)
        if self.proximity_sensor.nextState:
            self.proximity_sensor.nextState = False
            self.leaved()
            return
         if self.ir_sensor_right.nextState or self.ir_sensor_left.nextState:
            self.ir_sensor_right.nextState = False
            self.ir_sensor_right.nextState = False
            self.voted()
            return
        self.loopVoting()

    ##########################
    #  Transition callbacks  #
    ##########################

    def on_setup_ready(self): #TODO      
        # move steppers on 50%
        # move servos (command 1) drawing from one avaible routine 
        # show screen (or more than one) neutral (?)
        # play audio (or more than one) neutral (?)     

    def on_loopEngaging(self):
        time.sleep(1)

    def on_approached(self): #TODO
        # move steppers at 50%
        # move servos (command 1) depending on the voting routine
        # show screen (or more than one) depending on the voting routine
        # play audio (or more than one) depending on the voting routine

            
        
            
            
