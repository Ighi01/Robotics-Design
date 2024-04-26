import digitalio

class IRSensor:
    def __init__(self, pin):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.switch_to_input(pull=digitalio.Pull.UP)
        self.value = False
        self.counter = 0
        self.pin.irq_trigger(digitalio.EdgeRising, self.irq_callback)

    def irq_callback(self, pin):
        self.value = True
        self.counter += 1
