from robot.robot import Robot


def engaging_1(robot: Robot):
    robot.left.eye.neutral()
    robot.right.eye.neutral()
    
    #1    
    robot.left.mouth.open(30,0,Curve.QUADRATIC)
    robot.left.arm.raise_percent(90,72,0,Curve.CUBIC)
    robot.left.neck.look_away(30,0,Curve.QUADRATIC)
    robot.left.neck.look_down(15,0)
    
    robot.right.mouth.open(21,2,Curve.QUADRATIC)
    robot.right.arm.raise_percent(90,57,2,Curve.CUBIC)
    robot.right.neck.look_away(30,2,Curve.QUADRATIC)
    robot.right.neck.look_down(11,2)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    
    #2
    robot.left.mouth.close(30,0,Curve.QUADRATIC)
    robot.left.mouth.open(30,1,Curve.QUADRATIC)
    robot.left.arm.raise_half(64,1,Curve.BOUNCE)
    robot.left.arm.raise_percent(90,64,2,Curve.CUBIC)
    robot.left.neck.look_up(15,1)
    robot.left.neck.look_down(15,2)
    
    robot.right.mouth.close(21,2,Curve.QUADRATIC)
    robot.right.mouth.open(21,1,Curve.QUADRATIC)
    robot.right.arm.raise_half(64,3,Curve.BOUNCE)
    robot.right.arm.raise_percent(90,64,4,Curve.CUBIC)
    robot.right.neck.look_up(15,3)
    robot.right.neck.look_down(15,4)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    
    #3
    robot.left.mouth.close(30,0,Curve.QUADRATIC)
    robot.left.mouth.open(30,1,Curve.QUADRATIC)
    robot.left.arm.raise_half(64,1,Curve.BOUNCE)
    robot.left.arm.raise_percent(90,64,2,Curve.CUBIC)
    robot.left.neck.look_up(15,1)
    robot.left.neck.look_down(15,2)
    
    robot.right.mouth.close(21,2,Curve.QUADRATIC)
    robot.right.mouth.open(21,1,Curve.QUADRATIC)
    robot.right.arm.raise_half(64,3,Curve.BOUNCE)
    robot.right.arm.raise_percent(90,64,4,Curve.CUBIC)
    robot.right.neck.look_up(15,3)
    robot.right.neck.look_down(15,4)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    
    #4
    robot.left.mouth.close(30,0,Curve.QUADRATIC)
    robot.left.mouth.open(30,1,Curve.QUADRATIC)
    robot.left.arm.raise_half(64,1,Curve.BOUNCE)
    robot.left.arm.raise_percent(90,64,2,Curve.CUBIC)
    robot.left.neck.look_up(15,1)
    robot.left.neck.look_down(15,2)
    
    robot.right.mouth.open(21,2,Curve.QUADRATIC)
    robot.right.mouth.close(21,1,Curve.QUADRATIC)
    robot.right.arm.raise_half(64,3,Curve.BOUNCE)
    robot.right.arm.raise_percent(90,64,4,Curve.CUBIC)
    robot.right.neck.look_up(15,3)
    robot.right.neck.look_down(15,4)
    
    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
