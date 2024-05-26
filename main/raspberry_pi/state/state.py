from multiprocessing import Process

from statemachine import StateMachine, State

from robot.robot import Robot


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
    processes: list[Process]

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

    #######################
    #   State callbacks   #
    #######################

    def on_enter_setup(self):
        self.robot.connect_arduinos()

    def on_enter_engaging(self):
        pass

    def on_enter_feedback(self):
        pass

    def on_enter_voting(self):
        pass

    ##########################
    #  Transition callbacks  #
    ##########################

    def on_setup_ready(self):
        pass

    def on_loopEngaging(self):
        pass

    def on_approached(self):
        pass
