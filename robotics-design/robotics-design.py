from screen.screen import Screen
from servo.arduino import Arduino
from servo.servo import Servo
from digitalio import DigitalInOut
import board
from time import sleep


def main():
    left_screen = Screen(DigitalInOut(board.D17), DigitalInOut(board.D25), DigitalInOut(board.D24))
    right_screen = Screen(DigitalInOut(board.D27), DigitalInOut(board.D6), DigitalInOut(board.D5))
    arduino_0 = Arduino('/dev/ttyUSB0')
    servo_0 = Servo(arduino_0, 0)
    servo_1 = Servo(arduino_0, 1)
    servo_2 = Servo(arduino_0, 2)
    servo_3 = Servo(arduino_0, 3)

    print('Blanking screens')
    left_screen.blank()
    right_screen.blank()
    
    sleep(2)
    
    print('Showing sad face')
    left_screen.gif('static/gifs/sad.gif')
    right_screen.gif('static/gifs/sad.gif')
    
    sleep(2)
    
    print('Moving servos')
    servo_0.hi()
    servo_1.hi()
    servo_2.hi()
    servo_3.hi()
    
    sleep(2)
    
    print('Blanking screens')
    left_screen.blank()
    right_screen.blank()


if __name__ == '__main__':
    main()
