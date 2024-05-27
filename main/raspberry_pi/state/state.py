import sys
from multiprocessing import Process
from signal import signal, SIGTERM
import random
from time import sleep

from statemachine import StateMachine, State

from robot.robot import Robot
import state.routines as routines


class SM(StateMachine):
    """
    This class is a state machine that represents the different states of the voting process.
    Documentation on the order in which the callbacks are called can be found in
    https://python-statemachine.readthedocs.io/en/latest/actions.html#ordering
    """

    #################
    #  Definitions  #
    #################
    robot: Robot
    current_routine: Process
    left_votes: int
    right_votes: int
    trigger_distance: float = 10.0
    voting_timeout: int = 30
    idled: bool

    # These are the states of the state machine
    setup = State('setup', initial=True)
    engaging = State('Engaging')
    voting = State('Voting')
    feedback = State('Feedback')

    # These are the transitions of the state machine
    setup_ready = setup.to(engaging)
    loopEngaging = engaging.to.itself()
    loopVoting = voting.to.itself()
    approached = engaging.to(voting)
    leaved = voting.to(engaging)
    voted_engaging = engaging.to(feedback)
    voted = voting.to(feedback)
    feedbacked = feedback.to(engaging)

    # This is the constructor of the state machine
    def __init__(self, robot: Robot):
        self.robot = robot
        self.left_votes = 0
        self.right_votes = 0
        self.idled = False
        super(SM, self).__init__()
        
    ########################
    #   Utility functions  #
    ########################
    
    @property
    def percentages(self):
        if not self.left_votes and not self.right_votes:
            return 50, 50
        elif not self.left_votes:
            return 0, 100
        elif not self.right_votes:
            return 100, 0
        else:
            total_votes = self.left_votes + self.right_votes
            left_percentage = self.left_votes / total_votes
            right_percentage = self.right_votes / total_votes
            return left_percentage, right_percentage
    
    def execute_routine(self, routine: callable, args: tuple):
        self.current_routine = Process(target=routine, args=args)
        self.current_routine.start()
        

    #######################
    #   State callbacks   #
    #######################

    def on_enter_setup(self):
        print('Entered setup')
        self.robot.connect_arduinos()
        self.setup_ready()

    def on_enter_engaging(self):
        print('Entered engaging')
        routine = random.choice([routines.engaging_1, routines.engaging_2, routines.engaging_3]) if self.idled else routines.idle
        self.idled = not self.idled
        print(f'Selected engaging routine {routine.__name__}')
        self.execute_routine(routine, (self.robot, *self.percentages))
        print('Engaging routine started')
        while self.current_routine.is_alive():
            current_distance = self.robot.proximity_sensor.distance
            print(f'Current distance: {current_distance}')
            if current_distance < self.trigger_distance:
                self.approached()
                return
            else:
                sleep(1)
        print('Engaging routine finished')
        self.loopEngaging()

    def on_enter_voting(self):
        print('Entered voting!')
        self.execute_routine(routines.voting, (self.robot, *self.percentages))
        while self.current_routine.is_alive():
            sleep(1)
        print('No one there!')
        self.leaved()
        return
        

    def on_enter_feedback(self):
        pass

    ##########################
    #  Transition callbacks  #
    ##########################

    def on_setup_ready(self):
        print('Setup completed')

    def on_loopEngaging(self):
        pass

    def on_approached(self):
        print('Robot approached')
        self.current_routine.terminate()
        print('Current routine terminated')
