import digitalio

class IRSensor:
    def __init__(self, pin , state_machine):
        self.pin = digitalio.DigitalInOut(pin)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.switch_to_input(pull=digitalio.Pull.DOWN)
        self.counter = 0
        self.fsm = state_machine
        self.pin.irq_trigger(digitalio.EdgeRising, self.irq_callback)

    def irq_callback(self, pin):
        self.counter += 1

        if self.fsm.current_state = 'engaging' or self.fsm.current_state = 'voting':
            self.fsm.states[self.fsm.current_state].isFirst = True

        self.fsm.current_state = 'feedback'
