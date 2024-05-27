import RPi.GPIO as GPIO
import logging


log = logging.getLogger(__name__)

def do_nothing(_):
    pass


class IRSensor:
    pin: int
    bouncetime: int
    callback: callable = do_nothing

    def __init__(self, pin, bouncetime=100):
        self.pin = pin
        self.bouncetime = bouncetime

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
        self.callback.__call__()

    def set_callback(self, callback: callable):
        log.debug(f'Setting callback for pin {self.pin} to {callback.__name__}')
        self.callback = callback

    def remove_callback(self):
        self.callback = do_nothing
