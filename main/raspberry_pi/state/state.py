import logging
import sys
from multiprocessing import Process
from signal import signal, SIGTERM
import random
from time import time, sleep
import multiprocessing as mp

from statemachine import StateMachine, State

from robot.robot import Robot
import state.routines as routines


log = logging.getLogger(__name__)


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
    voting_timeout: mp.Process
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
    abandoned = voting.to(engaging)
    voted_engaging = engaging.to(feedback)
    voted_left = voting.to(feedback)
    voted_right = voting.to(feedback)
    feedbacked = feedback.to(engaging)

    # This is the constructor of the state machine
    def __init__(self, robot: Robot):
        self.robot = robot
        self.left_votes = 0
        self.right_votes = 0
        self.idled = False
        self.voting_timeout = None
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
        
    def interrupt_routine(self):
        self.current_routine.terminate()
        self.current_routine.join()
        
    def after_transition(self, event, source, target):
        if source.id != target.id:
            log.info(f"{source.id} --{event}--> {target.id}")
    
    def _call_abandoned(self):
        self.abandoned()
        
            
    def _voting_timeout(self, abandoned):
        log.debug('Starting timeout')
        sleep(5)
        log.debug('Timeout reached')
        abandoned()

    #######################
    #   State callbacks   #
    #######################

    def on_enter_setup(self):
        self.robot.connect_arduinos()
        self.setup_ready()

    def on_enter_engaging(self):
        routine = random.choice([routines.engaging_1, routines.engaging_2, routines.engaging_3]) if self.idled else routines.idle
        self.idled = not self.idled
        log.debug(f'Selected engaging routine {routine.__name__}')
        self.execute_routine(routine, (self.robot, *self.percentages))
        while self.current_routine.is_alive():
            current_distance = self.robot.proximity_sensor.distance
            log.debug(f'Current distance: {current_distance}')
            if current_distance < self.trigger_distance:
                self.approached()
                return
            else:
                sleep(1)
        self.loopEngaging()

    def on_enter_voting(self):
        self.robot.set_ir_callbacks(self.voted_left, self.voted_right)
        self.execute_routine(routines.voting, (self.robot, *self.percentages))
        self.voting_timeout = mp.Process(target=self._voting_timeout, args=(self._call_abandoned,))
        self.voting_timeout.start()

    def on_enter_feedback(self):
        log.debug(f'Feedback!')
        self.feedbacked()

    ##########################
    #  Transition callbacks  #
    ##########################

    def on_loopEngaging(self):
        pass

    def on_approached(self):
        self.interrupt_routine()
        
    def on_abandoned(self):
        self.interrupt_routine()
        self.robot.remove_ir_callbacks()
        self.idled = False
        
    def on_voted_left(self):
        self.left_votes += 1
        log.info(f'Voted left, left_votes={self.left_votes}, right_votes={self.right_votes}')
        self.robot.remove_ir_callbacks()
        self.voting_timeout.terminate()
        
    def on_voted_right(self):
        self.right_votes += 1
        log.info(f'Voted right, left_votes={self.left_votes}, right_votes={self.right_votes}')
        self.robot.remove_ir_callbacks()
        self.voting_timeout.terminate()
