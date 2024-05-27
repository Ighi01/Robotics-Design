import sys
from multiprocessing import Process
from signal import signal, SIGTERM
import random

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
    trigger_distance: int = 10

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
        super(SM, self).__init__()
        self.robot = robot
        
    ########################
    #   Utility functions  #
    ########################
    
    @property
    def percentages(self):
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
        random_engaging = random.choice([routines.engaging_1, routines.engaging_2, routines.engaging_3])
        print(f'Selected engaging routine {random_engaging.__name__}')
        self.execute_routine(random_engaging, (self.robot, *self.percentages))
        print('Engaging routine started')
        while self.current_routine.is_alive():
            current_distance = self.robot.proximity_sensor.get_distance()
            print(f'Current distance: {current_distance}')
            if self.robot.proximity_sensor.get_distance() < self.trigger_distance:
                self.approached()
            else:
                sleep(0.1)
        print('Engaging routine finished')
        self.loopEngaging()

    def on_enter_voting(self):
        print('Entered voting!')
        self.execute_routine(routines.voting, (self.robot, *self.percentages))
        

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
