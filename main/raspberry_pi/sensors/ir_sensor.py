import RPi.GPIO as GPIO
from statemachine import StateMachine

class IRSensor:
    pin: int
    machine: StateMachine
    bouncetime: int
    counter: int

    def __init__(self, pin, machine, bouncetime=100):
        self.pin = pin
        self.machine = machine
        self.bouncetime = bouncetime
        self.counter = 0

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.ir_callback, bouncetime=self.bouncetime)

    def ir_callback(self):
        self.counter = self.counter + 1
        if self.machine.getstate() == 'Engaging':
            self.machine.voted_engaging()
        if self.getstate() == 'Voting':
            self.machine.voted()