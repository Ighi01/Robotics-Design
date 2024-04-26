class Feedback:
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def run(self):
        print('Feedback state')
        if self.state_machine.proximity_distance is not None:
            print('Proximity Distance:', self.state_machine.proximity_distance, 'cm')
            if self.state_machine.proximity_distance > 10: 
                self.state_machine.current_state = 'engaging'
