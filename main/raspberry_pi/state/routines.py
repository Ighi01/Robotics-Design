from time import sleep

from components.curve import Curve
from robot.robot import Robot
from robot.sounds import Sounds


def engaging_1(robot: Robot):
    robot.left.eye.neutral()
    robot.right.eye.neutral()

    # 1
    robot.left.mouth.open(30, 0, Curve.QUADRATIC)
    robot.left.arm.raise_percent(90, 72, 0, Curve.CUBIC)
    robot.left.neck.look_away(30, 0, Curve.QUADRATIC)
    robot.left.neck.look_down(15, 0)

    robot.right.mouth.open(21, 2, Curve.QUADRATIC)
    robot.right.arm.raise_percent(90, 57, 2, Curve.CUBIC)
    robot.right.neck.look_away(30, 2, Curve.QUADRATIC)
    robot.right.neck.look_down(11, 2)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)

    # 2
    robot.left.mouth.close(30, 0, Curve.QUADRATIC)
    robot.left.mouth.open(30, 1, Curve.QUADRATIC)
    robot.left.arm.raise_half(64, 1, Curve.BOUNCE)
    robot.left.arm.raise_percent(90, 64, 2, Curve.CUBIC)
    robot.left.neck.look_up(15, 1)
    robot.left.neck.look_down(15, 2)

    robot.right.mouth.close(21, 2, Curve.QUADRATIC)
    robot.right.mouth.open(21, 1, Curve.QUADRATIC)
    robot.right.arm.raise_half(64, 3, Curve.BOUNCE)
    robot.right.arm.raise_percent(90, 64, 4, Curve.CUBIC)
    robot.right.neck.look_up(15, 3)
    robot.right.neck.look_down(15, 4)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)

    # 3
    robot.left.mouth.close(30, 0, Curve.QUADRATIC)
    robot.left.mouth.open(30, 1, Curve.QUADRATIC)
    robot.left.arm.raise_half(64, 1, Curve.BOUNCE)
    robot.left.arm.raise_percent(90, 64, 2, Curve.CUBIC)
    robot.left.neck.look_up(15, 1)
    robot.left.neck.look_down(15, 2)

    robot.right.mouth.close(21, 2, Curve.QUADRATIC)
    robot.right.mouth.open(21, 1, Curve.QUADRATIC)
    robot.right.arm.raise_half(64, 3, Curve.BOUNCE)
    robot.right.arm.raise_percent(90, 64, 4, Curve.CUBIC)
    robot.right.neck.look_up(15, 3)
    robot.right.neck.look_down(15, 4)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)

    # 4
    robot.left.mouth.close(30, 0, Curve.QUADRATIC)
    robot.left.mouth.open(30, 1, Curve.QUADRATIC)
    robot.left.arm.raise_half(64, 1, Curve.BOUNCE)
    robot.left.arm.raise_percent(90, 64, 2, Curve.CUBIC)
    robot.left.neck.look_up(15, 1)
    robot.left.neck.look_down(15, 2)

    robot.right.mouth.open(21, 2, Curve.QUADRATIC)
    robot.right.mouth.close(21, 1, Curve.QUADRATIC)
    robot.right.arm.raise_half(64, 3, Curve.BOUNCE)
    robot.right.arm.raise_percent(90, 64, 4, Curve.CUBIC)
    robot.right.neck.look_up(15, 3)
    robot.right.neck.look_down(15, 4)

    robot.send_servo_movements()
    robot.left.arduino.wait_servos()
    robot.left.mouth.say(Sounds.GRRR)
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)


def engaging_2(robot: Robot):
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
    robot.left.eye.angry_1()
    robot.right.arduino.wait_servos()
    robot.right.mouth.say(Sounds.GRRR)
    robot.right.eye.angry_1()

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
