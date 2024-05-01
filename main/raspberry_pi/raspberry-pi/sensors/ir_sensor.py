import RPi.GPIO as GPIO

class IRSensor:
    counter: int
    
    def __init__(self, pin, state_machine):
        self.counter = 0
        self.fsm = state_machine
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.irq_callback)

    def irq_callback(self, pin):
        self.counter += 1

        if self.fsm.current_state == 'engaging' or self.fsm.current_state == 'voting':
            self.fsm.states[self.fsm.current_state].isFirst = True

        self.fsm.current_state = 'feedback'
