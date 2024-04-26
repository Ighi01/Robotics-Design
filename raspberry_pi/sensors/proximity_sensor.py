import pulseio
import digitalio
import time
import threading

class ProximitySensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = digitalio.DigitalInOut(trigger_pin)
        self.trigger_pin.direction = digitalio.Direction.OUTPUT
        self.echo_pin = pulseio.PulseIn(echo_pin, maxlen=1)
        self.echo_pin.clear()
        self.distance = None

    def measure_distance_task(self):
        while True:
            self.trigger_pin.value = True
            time.sleep(0.00001)
            self.trigger_pin.value = False
            self.echo_pin.clear()

            while not self.echo_pin:
                pass
            start_time = time.monotonic()
            while self.echo_pin:
                pass
            end_time = time.monotonic()

            pulse_duration = end_time - start_time

            distance = pulse_duration * 34300 / 2 
            self.distance = distance
            time.sleep(0.1)
