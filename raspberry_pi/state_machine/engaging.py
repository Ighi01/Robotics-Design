class Engaging:
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def run(self):
        print('Engaging state')
        if self.state_machine.ir_sensor1_state and not self.state_machine.ir_sensor2_state:
            self.state_machine.current_state = 'voting'

