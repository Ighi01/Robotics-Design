from time import sleep

from components.curve import Curve
from robot.robot import Robot
from robot.sounds import Sounds


def engaging_1(robot: Robot):
    robot.left.eye.neutral()
    robot.right.eye.neutral()
    
    robot.right.arm.raise_half(80, 0, Curve.QUADRATIC)
    robot.left.arm.raise_half(80, 0, Curve.QUADRATIC)
    
    robot.left.eye.raise_percent(50, 100, 5, 100)
    robot.right.eye.raise_percent(50, 100, 5, 100)
    
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
        sleep(0.5)
        
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
        sleep(0.5)
        
        robot.left.mouth.open(80, 0, Curve.QUADRATIC)
        robot.left.arm.raise_full(80, 0, Curve.CUBIC)
        robot.left.neck.look_away(60, 0, Curve.QUADRATIC)
        robot.left.neck.look_down(30, 0)
        robot.left.mouth.say(Sounds.AAAA)
        
        robot.left.arduino.send_servo_movements()
        robot.right.arduino.wait_servos()
        sleep(0.5)
        
        robot.right.mouth.close(30, 0, Curve.QUADRATIC)
        robot.right.arm.raise_half(40, 0, Curve.BOUNCE)
        robot.right.neck.look_front(30, 0, Curve.QUADRATIC)
        robot.right.neck.look_center(15, 0)
        
        robot.right.arduino.send_servo_movements()
        robot.left.arduino.wait_servos()
        sleep(0.5)
        
        robot.left.mouth.close(80, 0, Curve.QUADRATIC)
        robot.left.arm.raise_half(80, 0, Curve.BOUNCE)
        robot.left.neck.look_front(60, 0, Curve.QUADRATIC)
        robot.left.neck.look_center(30, 0)
        
        robot.left.arduino.send_servo_movements()     
        robot.right.arduino.wait_servos() 
        robot.left.arduino.wait_servos()
        sleep(0.5)
        

def engaging_2(robot: Robot): #TODO BETTER
    robot.left.eye.neutral()
    robot.right.eye.neutral()

    # 1
    robot.left.neck.look_to_other(75, curve=Curve.QUADRATIC)
    robot.left.eye.raise_percent(50, 100, 0, 100)

    robot.right.neck.look_to_other(75, curve=Curve.QUADRATIC)
    robot.right.eye.raise_percent(50, 100, 0, 100)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.left.eye.angry_2()
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    robot.right.eye.angry_2()

    # 2
    robot.left.neck.look_down(15, 2)
    robot.left.neck.look_center(15, 1)

    robot.right.eye.raise_percent(100, 100, 0, 100)

    robot.left.arduino.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_stepper()
    sleep(1)
    robot.right.eye.raise_percent(50, 100, 0, 100)

    # 3
    robot.left.neck.look_up(15, 2)
    robot.left.neck.look_away(360, 2, Curve.QUADRATIC)
    robot.left.neck.look_front(90, 2, Curve.QUADRATIC)

    robot.right.neck.look_up(15, 2)
    robot.right.neck.look_away(360, 2, Curve.QUADRATIC)
    robot.right.neck.look_front(90, 2, Curve.QUADRATIC)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.right.arduino.wait_servos()

    # 4
    robot.left.mouth.open(30, 1, Curve.QUADRATIC)
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
    
    
def engaging_3(robot: Robot, int: left_percentage, int: right_percentage):
    robot.left.eye.neutral()
    robot.right.eye.neutral()
    
    robot.left.eye.raise_percent(left_percentage, 100, 5, 100)
    robot.right.eye.raise_percent(right_percentage, 100, 5, 100)
    
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
    
    sleep(0.5)
    
    robot.left.mouth.say(Sounds.YUM)
    robot.left.eye.raise_percent(left_percentage + 25 if left_percentage + 25 < 100 else 100 , 100, 5, 100)
    robot.left.eye.happy_1()
    robot.left.mouth.ñamñam(5,45,Curve.QUADRATIC,0)
    robot.left.arduino.send_servo_movements()
    
    sleep(2)
    robot.right.eye.comp()
    robot.right.eye.raise_percent(right_percentage - 25 if left_percentage - 25 > 0 else 0 , 100, 0, 100)
    robot.left.mouth.say(Sounds.UHOH)
    
    robot.left.arduino.wait_servos()
    
    
#def engaging_3(robot: Robot, int: left_percentage, int: right_percentage):
    
