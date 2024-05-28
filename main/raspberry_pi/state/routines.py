import logging
from time import sleep
from components.curve import Curve
from robot.robot import Robot
from robot.sounds import Sounds
from signal import signal, SIGTERM
import pygame
from random import randint


log = logging.getLogger(__name__)


def setup(robot: Robot):
    def handler(signum, frame):
        robot.stop_eyes()
        exit(0)
    signal(SIGTERM, handler)
    robot.start_eyes()
    robot.start_voice()

    
def reset(robot: Robot, left_percentage: int, right_percentage: int):
    reset_screen(robot, left_percentage, right_percentage)
    reset_stepper_fixed(robot, left_percentage, right_percentage)
    reset_servo(robot, left_percentage, right_percentage)
    
def reset_screen(robot: Robot, left_percentage: int, right_percentage: int):
    robot.left.eye.neutral()
    robot.right.eye.neutral()
    
def reset_stepper_fixed(robot: Robot, left_percentage: int, right_percentage: int):
    robot.left.eye.raise_percent(50, 100, 0, 100)
    sleep(0.5)
    robot.right.eye.raise_percent(50, 100, 0, 100)
    
def reset_stepper_bouncing(robot: Robot, left_percentage: int, right_percentage: int):
    robot.left.eye.raise_percent(50, 100, 5, 100)
    sleep(0.5)
    robot.right.eye.raise_percent(50, 100, 5, 100)
    
def set_stepper_fixed_on_percentage(robot: Robot, left_percentage: int, right_percentage: int):
    robot.left.eye.raise_percent(left_percentage, 100, 0, 100)
    sleep(0.5)
    robot.right.eye.raise_percent(right_percentage, 100, 0, 100)
    
def set_stepper_bouncing_on_percentage(robot: Robot, left_percentage: int, right_percentage: int):
    robot.left.eye.raise_percent(left_percentage, 100, 5, 100)
    sleep(0.5)
    robot.right.eye.raise_percent(right_percentage, 100, 5, 100)

def reset_servo(robot: Robot, left_percentage: int, right_percentage: int):    
    robot.left.mouth.close(100)
    robot.left.arm.lower(100)
    robot.left.neck.look_front(100)
    robot.left.neck.look_center(30)
        
    robot.right.mouth.close(100)
    robot.right.arm.lower(100)
    robot.right.neck.look_front(100)
    robot.right.neck.look_center(30)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()
    
def idle(robot: Robot, left_percentage: int, right_percentage: int):
    setup(robot)
    reset_screen(robot, left_percentage, right_percentage)
    reset_servo(robot, left_percentage, right_percentage)    
    reset_stepper_bouncing(robot, left_percentage, right_percentage)
    time = randint(30, 120)
    log.debug(f'Idling for {time} seconds')
    sleep(time)
    
def engaging_1(robot: Robot, left_percentage: int, right_percentage: int): 
    setup(robot)
    reset_screen(robot, left_percentage, right_percentage)
    
    robot.right.arm.raise_half(80, 0, Curve.QUADRATIC)
    robot.left.arm.raise_half(80, 0, Curve.QUADRATIC)
    
    reset_stepper_bouncing(robot, left_percentage, right_percentage)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()
    
    times = 4
    
    for _ in range(times):
        
        robot.left.mouth.open(80, 0, Curve.QUADRATIC)
        robot.left.arm.raise_full(80, 0, Curve.CUBIC)
        robot.left.neck.look_away(60, 0, Curve.QUADRATIC)
        robot.left.neck.look_down(30, 0)
        robot.left.mouth.say(Sounds.AAAA)
        
        robot.left.arduino.send_servo_movements()
        robot.left.arduino.wait_servos()
        sleep(1)
        
        robot.left.mouth.close(80, 0, Curve.QUADRATIC)
        robot.left.arm.raise_half(80, 0, Curve.BOUNCE)
        robot.left.neck.look_front(60, 0, Curve.QUADRATIC)
        robot.left.neck.look_center(30, 0)

        robot.right.mouth.open(30, 0, Curve.QUADRATIC)
        robot.right.arm.raise_full(40, 0, Curve.CUBIC)
        robot.right.neck.look_away(30, 0, Curve.QUADRATIC)
        robot.right.neck.look_down(15, 0)
        robot.right.mouth.say(Sounds.AAAA)

        robot.send_servo_movements()
        robot.left.arduino.wait_servos()
        sleep(1)
        
        robot.left.mouth.open(80, 0, Curve.QUADRATIC)
        robot.left.arm.raise_full(80, 0, Curve.CUBIC)
        robot.left.neck.look_away(60, 0, Curve.QUADRATIC)
        robot.left.neck.look_down(30, 0)
        robot.left.mouth.say(Sounds.AAAA)
        
        robot.left.arduino.send_servo_movements()
        robot.right.arduino.wait_servos()
        sleep(1)
        
        robot.right.mouth.close(30, 0, Curve.QUADRATIC)
        robot.right.arm.raise_half(40, 0, Curve.BOUNCE)
        robot.right.neck.look_front(30, 0, Curve.QUADRATIC)
        robot.right.neck.look_center(15, 0)
        
        robot.right.arduino.send_servo_movements()
        robot.left.arduino.wait_servos()
        sleep(1)
        
        robot.left.mouth.close(80, 0, Curve.QUADRATIC)
        robot.left.arm.raise_half(80, 0, Curve.BOUNCE)
        robot.left.neck.look_front(60, 0, Curve.QUADRATIC)
        robot.left.neck.look_center(30, 0)
        
        robot.left.arduino.send_servo_movements()     
        robot.right.arduino.wait_servos() 
        robot.left.arduino.wait_servos()
        sleep(1)
        

def engaging_2(robot: Robot, left_percentage: int, right_percentage: int): #TODO : aggiungere suono verso la fine 
    setup(robot)
    reset_screen(robot, left_percentage, right_percentage)
    
    reset_stepper_fixed(robot, left_percentage, right_percentage)
    
    robot.left.neck.look_to_other(75, curve=Curve.QUADRATIC)
    robot.right.neck.look_to_other(75, curve=Curve.QUADRATIC)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.left.eye.angry_2()
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    robot.right.eye.angry_2()
    
    sleep(2)
    
    robot.right.eye.raise_percent(100, 100, 0, 100)
    
    robot.left.neck.look_down(15, 0)
    robot.left.neck.look_up(15, 2)
    robot.left.neck.look_center(15, 2)

    robot.left.arduino.send_servo_movements()
    robot.left.arduino.wait_servos()
    
    sleep(1)
    
    robot.right.eye.raise_percent(50, 100, 0, 100)
    robot.right.neck.look_up(15, 0)
    robot.right.neck.look_down(15, 2)
    robot.right.neck.look_center(15, 2)
    
    robot.right.arduino.send_servo_movements()
    robot.right.arduino.wait_servos()
    
    sleep(1)

    robot.left.neck.look_up(15, 0)
    robot.left.neck.look_away(360, 2, Curve.QUADRATIC)
    robot.left.neck.look_front(90, 2, Curve.QUADRATIC)

    robot.right.neck.look_up(15, 0)
    robot.right.neck.look_away(360, 2, Curve.QUADRATIC)
    robot.right.neck.look_front(90, 2, Curve.QUADRATIC)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()
    
    sleep(1)

    robot.left.mouth.open(30, 0, Curve.QUADRATIC)
    robot.left.arm.raise_percent(90, 64, 2, Curve.CUBIC)

    robot.right.mouth.open(21, 2, Curve.QUADRATIC)
    robot.right.arm.raise_percent(90, 64, 4, Curve.CUBIC)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.left.eye.neutral()
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    robot.left.eye.neutral()    
    
def engaging_3(robot: Robot, left_percentage: int, right_percentage: int): #TODO: musica si interrompe troppo presto
    setup(robot)
    
    reset_screen(robot, left_percentage, right_percentage)
    
    set_stepper_bouncing_on_percentage(robot, left_percentage, right_percentage)
    
    robot.right.arm.raise_half(28, 0, Curve.CUBIC)
    robot.right.neck.look_away(22, 0, Curve.QUADRATIC)
    robot.right.neck.look_down(11, 0)
    robot.right.mouth.say(Sounds.INHALE)
    
    robot.right.arduino.send_servo_movements()
    robot.right.arduino.wait_servos()
    
    robot.right.mouth.open_half(20, 0, Curve.QUADRATIC)
    
    robot.right.arduino.send_servo_movements()
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.EXHALE)
    
    sleep(1.5)
    
    robot.right.eye.raise_percent(right_percentage, 100, 0, 100)
    robot.right.eye.angry_1()
    robot.right.mouth.say(Sounds.COUGH)
    robot.right.mouth.close(100,curve=Curve.BOUNCE)
    robot.right.neck.look_down(30,0,curve=Curve.BOUNCE)
    robot.right.arm.raise_full(100,0,curve=Curve.BOUNCE)
    robot.right.arm.raise_half(100,0,curve=Curve.BOUNCE)
    robot.right.arm.raise_full(100,0,curve=Curve.BOUNCE)
    robot.right.arm.raise_half(100,0,curve=Curve.BOUNCE)
    robot.right.arm.raise_full(100,0,curve=Curve.BOUNCE)
    
    robot.right.arduino.send_servo_movements()
    robot.right.arduino.wait_servos()    
    
    robot.left.eye.raise_percent(left_percentage + 75 if left_percentage + 75 < 100 else 100 , 100, 5, 100)
    
    sleep(5)
    robot.left.eye.happy_1()
    
    times = 2
    
    for _ in range(times):
        robot.left.mouth.open_percent(60, 30, 0 , Curve.QUADRATIC)
        robot.left.mouth.close(30, 0, Curve.QUADRATIC)
            
    robot.left.arduino.send_servo_movements()
    
    sleep(0.5)
    
    robot.left.mouth.say(Sounds.YUM)
        
    robot.right.eye.raise_percent(right_percentage - 75 if right_percentage - 75 > 0 else 0 , 100, 0, 100)
    
    sleep(2)
    robot.right.eye.comp()
    robot.right.mouth.say(Sounds.UHOH)
    robot.left.arduino.wait_servos()
    sleep(3)
    
    
def voting(robot: Robot, left_percentage: int, right_percentage: int):
    setup(robot)
    
    reset_screen(robot, left_percentage, right_percentage)
    reset_servo(robot, left_percentage, right_percentage)
    reset_stepper_fixed(robot, left_percentage, right_percentage)
    
    robot.left.mouth.open(80,curve=Curve.BOUNCE)
    robot.left.neck.look_up(30,0,curve=Curve.BOUNCE)
    
    robot.right.mouth.open(60,curve=Curve.BOUNCE)
    robot.right.neck.look_up(30,0,curve=Curve.BOUNCE)
    
    robot.send_servo_movements()
    robot.right.arduino.wait_servos() 
    robot.left.arduino.wait_servos() 
    
    robot.left.eye.comp()
    robot.right.eye.comp()
    
    times = 4
    
    for _ in range(times):
        sleep(5)
        robot.left.neck.turn_head_horizontal(50,100)
        robot.left.neck.turn_head_horizontal(10,100)
        robot.left.neck.turn_head_horizontal(30,100)
        
        robot.right.neck.turn_head_horizontal(170,100)
        robot.right.neck.turn_head_horizontal(130,100)
        robot.right.neck.turn_head_horizontal(150,100)      
        
        robot.send_servo_movements()
        robot.right.arduino.wait_servos() 
        robot.left.arduino.wait_servos() 
        
        robot.left.arm.raise_full(50)
        robot.right.arm.raise_full(50)    
        
        robot.send_servo_movements()
        robot.right.arduino.wait_servos() 
        robot.left.arduino.wait_servos() 
        
        robot.left.arm.lower(50)
        robot.right.arm.lower(50)
        
        robot.send_servo_movements()
        robot.right.arduino.wait_servos() 
        robot.left.arduino.wait_servos() 
    
    
def feedback_left(robot: Robot, left_percentage: int, right_percentage: int):
    reset_screen(robot, left_percentage, right_percentage)
    robot.left.neck.look_center(30, 0)
    robot.right.neck.look_center(30, 0)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()
    
    robot.left.mouth.say(Sounds.EATING)
    robot.right.mouth.close(100, 0, Curve.QUADRATIC)
    robot.left.mouth.ñamñam(6,160, Curve.QUADRATIC,0)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()
    
def feedback_right(robot: Robot, left_percentage: int, right_percentage: int):
    reset_screen(robot, left_percentage, right_percentage)
    set_stepper_fixed_on_percentage(robot, left_percentage, right_percentage)
    robot.left.neck.look_center(30, 0)
    robot.right.neck.look_center(30, 0)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()
    
    robot.right.mouth.say(Sounds.EATING)
    robot.left.mouth.close(100, 0, Curve.QUADRATIC)
    robot.right.mouth.ñamñam(6,120, Curve.QUADRATIC,0)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()
    
def feedback_right_1(robot: Robot, left_percentage: int, right_percentage: int):
    setup(robot)
    feedback_right(robot, left_percentage, right_percentage)
    
    robot.right.neck.look_to_other(300, curve=Curve.QUADRATIC)

    robot.right.arduino.send_servo_movements()
    robot.right.arduino.wait_servos()
    
    robot.right.mouth.open(20, 0, Curve.QUADRATIC)
    robot.right.mouth.say(Sounds.BURP)
        
    robot.right.arduino.send_servo_movements()
    robot.right.arduino.wait_servos()
    
    sleep(0.5)
    
    robot.right.eye.happy_1()
    robot.left.mouth.say(Sounds.BLEAH)
    robot.left.eye.angry_1()
    
    sleep(0.5)
    
    robot.left.neck.look_away(500, curve=Curve.BOUNCE)
    robot.left.neck.look_up(30, curve=Curve.BOUNCE)
    
    robot.left.arduino.send_servo_movements()
    robot.left.arduino.wait_servos()
    
def feedback_right_2(robot: Robot, left_percentage: int, right_percentage: int):
    setup(robot)
    feedback_right(robot, left_percentage, right_percentage)
    
    robot.right.neck.look_to_other(500, curve=Curve.BOUNCE)
    robot.left.neck.look_to_other(200)

    robot.send_servo_movements()
    robot.right.arduino.wait_servos()
    robot.left.arduino.wait_servos()
    
    robot.right.mouth.say(Sounds.EVIL_LAUGH)
    robot.right.eye.happy_1()
    
    sleep(1)
    
    robot.left.neck.look_away(500, curve=Curve.BOUNCE)
    robot.left.neck.look_down(30, curve=Curve.BOUNCE)
    
    robot.left.mouth.say(Sounds.CRYING)
    robot.left.eye.sad()
    
    robot.left.arduino.send_servo_movements()
    robot.left.arduino.wait_servos()
    
def feedback_right_3(robot: Robot, left_percentage: int, right_percentage: int):
    setup(robot)
    feedback_right(robot, left_percentage, right_percentage)
    
    robot.left.neck.look_to_other(75, curve=Curve.QUADRATIC)
    robot.right.neck.look_to_other(75, curve=Curve.QUADRATIC)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()   
    
    robot.right.eye.raise_percent(right_percentage + 75 if right_percentage + 75 < 100 else 100 , 100, 5, 100)
    robot.left.eye.raise_percent(left_percentage - 75 if left_percentage - 75 > 0 else 0 , 100, 5, 100)
    
    sleep(1)
    
    robot.right.mouth.say(Sounds.EVIL_LAUGH)
    robot.right.eye.angry_1()
    
    sleep(1)
    
    robot.left.mouth.say(Sounds.UHOH)
    robot.left.eye.comp()
    
def feedback_left_1(robot: Robot, left_percentage: int, right_percentage: int):
    setup(robot)
    feedback_left(robot, left_percentage, right_percentage)
    
    robot.left.neck.look_to_other(75, curve=Curve.QUADRATIC)
    robot.right.neck.look_to_other(75, curve=Curve.QUADRATIC)

    robot.send_servo_movements()
    robot.right.arduino.wait_servos()
    robot.left.arduino.wait_servos()
    
    robot.right.eye.raise_percent(right_percentage + 75 if right_percentage + 75 < 100 else 100 , 100, 5, 100)
    robot.left.eye.raise_percent(left_percentage - 75 if left_percentage - 75 > 0 else 0 , 100, 5, 100)
    
    robot.left.mouth.say(Sounds.HIGH_LAUGH)
    
    sleep(1)
    
    robot.right.mouth.say(Sounds.GRUMBLE)
    
    robot.right.arduino.wait_stepper()
    robot.left.arduino.wait_stepper()
    
def feedback_left_2(robot: Robot, left_percentage: int, right_percentage: int):
    setup(robot)
    feedback_left(robot, left_percentage, right_percentage)
    
    robot.left.neck.look_to_other(400, curve=Curve.QUADRATIC)

    robot.left.arduino.send_servo_movements()
    robot.left.arduino.wait_servos()
    
    sleep(0.5)
    
    robot.left.mouth.say(Sounds.YUMMY)
    robot.left.eye.happy_1()
    
    sleep(4)
    
    robot.right.neck.look_to_other(500, curve=Curve.BOUNCE)
    
    robot.right.arduino.send_servo_movements()
    robot.right.arduino.wait_servos()
    
    sleep(0.5)
        
    robot.right.mouth.say(Sounds.BLEEP)
    robot.right.eye.angry_2()
    
    sleep(2)
    
    times = 3
    
    for _ in range(times):
        robot.right.arm.raise_percent(70,150,0,Curve.BOUNCE)    
        robot.right.arduino.send_servo_movements()
        robot.right.arduino.wait_servos()
        robot.right.arm.lower(150,0,Curve.BOUNCE)   
        robot.right.arduino.send_servo_movements()
        robot.right.arduino.wait_servos()
        sleep(0.5)
        
def feedback_left_3(robot: Robot, left_percentage: int, right_percentage: int):
    setup(robot)
    feedback_left(robot, left_percentage, right_percentage)
    setup(robot)
    reset_screen(robot, left_percentage, right_percentage)
    
    set_stepper_fixed_on_percentage(robot, left_percentage, right_percentage)
    
    robot.left.neck.look_to_other(400, curve=Curve.QUADRATIC)

    robot.left.arduino.send_servo_movements()
    robot.left.arduino.wait_servos()
    
    sleep(0.5)
    
    robot.left.mouth.say(Sounds.RASP)
    robot.left.eye.happy_2()
    
    sleep(4)
    
    robot.right.neck.look_away(500, curve=Curve.BOUNCE)
    robot.right.neck.look_down(30, curve=Curve.BOUNCE)
    
    robot.right.arduino.send_servo_movements()
    robot.right.arduino.wait_servos()
    
    sleep(0.5)
        
    robot.right.mouth.say(Sounds.ANGRY)
    robot.right.eye.angry_2()
    
    sleep(2)
    
    times = 3
    
    for _ in range(times):
        robot.right.arm.raise_percent(70,150,0,Curve.BOUNCE)    
        robot.right.arduino.send_servo_movements()
        robot.right.arduino.wait_servos()
        robot.right.arm.lower(150,0,Curve.BOUNCE)   
        robot.right.arduino.send_servo_movements()
        robot.right.arduino.wait_servos()
        sleep(0.5)