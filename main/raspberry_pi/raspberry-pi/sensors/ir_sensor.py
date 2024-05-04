import RPi.GPIO as GPIO


class IRSensor:
    pin: int
    callback: callable
    bouncetime: int

    def __init__(self, pin, callback, bouncetime=100):
        self.pin = pin
        self.callback = callback
        self.bouncetime = bouncetime

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.callback, bouncetime=self.bouncetime)
