import RPi.GPIO as GPIO
import logging


log = logging.getLogger(__name__)

def do_nothing(*args):
    pass

def trip(self):
    self.tripped = True


class IRSensor:
    pin: int
    bouncetime: int
    callback: callable = do_nothing
    tripped: bool

    def __init__(self, pin, bouncetime=100):
        self.pin = pin
        self.bouncetime = bouncetime
        self.tripped = False

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(
            self.pin,
            GPIO.FALLING,
            callback=self.callback_func,
            bouncetime=self.bouncetime
        )
    
    def callback_func(self, *args):
        self.callback(self)

    def activate(self):
        self.callback = trip
        self.tripped = False
        log.debug(f'Activated IR sensor on pin {self.pin}')

    def deactivate(self):
        self.callback = do_nothing
        log.debug(f'Deactivated IR sensor on pin {self.pin}')
