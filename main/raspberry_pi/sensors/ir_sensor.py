import RPi.GPIO as GPIO
from statemachine import StateMachine

class IRSensor:
    pin: int
    nextState: bool
    bouncetime: int
    counter: int

    def __init__(self, pin, bouncetime=100):
        self.pin = pin
        self.bouncetime = bouncetime
        self.counter = 0
        self.nextState = False

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.ir_callback, bouncetime=self.bouncetime)

    def ir_callback(self):
        self.counter = self.counter + 1
        self.nextState = True