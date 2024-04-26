class Engaging:
    def __init__(self, state_machine):
        self.fsm = state_machine

    def run(self):
        print('Engaging state')
        #TODO: do the routines

        #Example of code
        if self.state_machine.proximity_distance is not None:
            print('Proximity Distance:', self.state_machine.proximity_distance, 'cm')
            if self.state_machine.proximity_distance < 40: 
                self.state_machine.current_state = 'voting'

