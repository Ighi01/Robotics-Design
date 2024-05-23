import RPi.GPIO as GPIO


def do_nothing(_):
    pass


class IRSensor:
    pin: int
    bouncetime: int
    callback: callable = None

    def __init__(self, pin, bouncetime=100):
        self.pin = pin
        self.bouncetime = bouncetime

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(
            self.pin,
            GPIO.FALLING,
            callback=self.callback if self.callback is not None else do_nothing,
            bouncetime=self.bouncetime
        )

    def set_callback(self, callback: callable):
        self.callback = callback
        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(
            self.pin,
            GPIO.FALLING,
            callback=self.callback,
            bouncetime=self.bouncetime
        )