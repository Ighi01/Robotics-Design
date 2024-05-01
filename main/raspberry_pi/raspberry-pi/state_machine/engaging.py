import random


class Engaging:
    def __init__(self, state_machine):
        self.fsm = state_machine
        # TODO : define real routines
        routine1 = {
            0: [[0, 0, 100], [90, 1, 100], [180, 2, 100], [270, 3, 20], [0, 4, 0]],
            1: [[0, 0, 200], [45, 3, 200], [90, 4, 200], [135, 5, 200], [180, 6, 200], [225, 7, 200], [0, 8, 20]],
            2: [[0, 0, 150], [180, 2, 150], [0, 3, 150], [180, 4, 20], [0, 5, 0]],
            3: [[0, 0, 180], [90, 2, 180], [180, 4, 20], [0, 5, 0]],
            4: [[0, 0, 120], [45, 1, 120], [90, 2, 120], [135, 3, 120], [180, 4, 120], [0, 5, 20]],
            5: [[0, 0, 250], [90, 3, 250], [180, 5, 250], [270, 7, 20], [0, 8, 0]],
            6: [[0, 0, 80], [180, 2, 80], [0, 3, 80], [180, 4, 80], [0, 5, 80], [180, 6, 80], [0, 7, 20]],
            7: [[0, 0, 220], [90, 3, 220], [180, 5, 220], [270, 7, 20], [0, 8, 0]],
            8: [[0, 0, 300], [90, 4, 300], [180, 6, 20], [0, 7, 0]],
            9: [[0, 0, 100], [45, 1, 100], [90, 2, 100], [135, 3, 100], [180, 4, 100], [225, 5, 100], [270, 6, 100],
                [315, 7, 100], [0, 8, 20]],
            10: [[0, 0, 180], [180, 2, 180], [0, 4, 180], [180, 6, 90], [0, 7, 0]]
        }

        routine2 = {
            0: [[0, 0, 100], [90, 1, 100], [180, 2, 100], [270, 3, 20], [0, 4, 0]],
            1: [[0, 0, 200], [45, 3, 200], [90, 4, 200], [135, 5, 200], [180, 6, 200], [225, 7, 200], [0, 8, 20]],
            2: [[0, 0, 150], [180, 2, 150], [0, 3, 150], [180, 4, 20], [0, 5, 0]],
            3: [[0, 0, 180], [90, 2, 180], [180, 4, 20], [0, 5, 0]],
            4: [[0, 0, 120], [45, 1, 120], [90, 2, 120], [135, 3, 120], [180, 4, 120], [0, 5, 20]],
            5: [[0, 0, 250], [90, 3, 250], [180, 5, 250], [270, 7, 20], [0, 8, 0]],
            6: [[0, 0, 80], [180, 2, 80], [0, 3, 80], [180, 4, 80], [0, 5, 80], [180, 6, 80], [0, 7, 20]],
            7: [[0, 0, 220], [90, 3, 220], [180, 5, 220], [270, 7, 20], [0, 8, 0]],
            8: [[0, 0, 300], [90, 4, 300], [180, 6, 20], [0, 7, 0]],
            9: [[0, 0, 100], [45, 1, 100], [90, 2, 100], [135, 3, 100], [180, 4, 100], [225, 5, 100], [270, 6, 100],
                [315, 7, 100], [0, 8, 20]],
            10: [[0, 0, 180], [180, 2, 180], [0, 4, 180], [180, 6, 90], [0, 7, 0]]
        }

        routine3 = {
            0: [[0, 0, 100], [90, 1, 100], [180, 2, 100], [270, 3, 20], [0, 4, 0]],
            1: [[0, 0, 200], [45, 3, 200], [90, 4, 200], [135, 5, 200], [180, 6, 200], [225, 7, 200], [0, 8, 20]],
            2: [[0, 0, 150], [180, 2, 150], [0, 3, 150], [180, 4, 20], [0, 5, 0]],
            3: [[0, 0, 180], [90, 2, 180], [180, 4, 20], [0, 5, 0]],
            4: [[0, 0, 120], [45, 1, 120], [90, 2, 120], [135, 3, 120], [180, 4, 120], [0, 5, 20]],
            5: [[0, 0, 250], [90, 3, 250], [180, 5, 250], [270, 7, 20], [0, 8, 0]],
            6: [[0, 0, 80], [180, 2, 80], [0, 3, 80], [180, 4, 80], [0, 5, 80], [180, 6, 80], [0, 7, 20]],
            7: [[0, 0, 220], [90, 3, 220], [180, 5, 220], [270, 7, 20], [0, 8, 0]],
            8: [[0, 0, 300], [90, 4, 300], [180, 6, 20], [0, 7, 0]],
            9: [[0, 0, 100], [45, 1, 100], [90, 2, 100], [135, 3, 100], [180, 4, 100], [225, 5, 100], [270, 6, 100],
                [315, 7, 100], [0, 8, 20]],
            10: [[0, 0, 180], [180, 2, 180], [0, 4, 180], [180, 6, 90], [0, 7, 0]]
        }
        self.routines = [routine1, routine2, routine3]
        self.current_routine_index = None
        self.isFirst = True

    def run(self):
        print('Engaging state')

        # NECK ROUTINE
        if self.isFirst:
            if self.fsm.ir_sensor1_counter == 0 and self.fsm.ir_sensor2_counter == 0:
                stepper_movements = {
                    0: [50, 100, 3, 200],
                    1: [50, 100, 3, 200]
                }
            else:
                stepper_movements = {
                    0: (
                    self.fsm.ir_sensor1.counter / (self.fsm.ir_sensor1.counter + self.fsm.ir_sensor2.counter), 100, 3,
                    200),
                    1: (
                    self.fsm.ir_sensor2.counter / (self.fsm.ir_sensor1.counter + self.fsm.ir_sensor2.counter), 100, 3,
                    200)
                }

            self.fsm.moveMultipleStepper(stepper_movements)

        # ARM ROUTINE
        if self.isFirst:
            random_index = random.randint(0, len(self.routines) - 1)
            while self.current_routine_index == random_index:
                random_index = random.randint(0, len(self.routines) - 1)
            self.current_routine_index = random_index
            self.fsm.moveMultipleServo(self.routines[self.current_routine_index])
        else:
            current_indexes = list(self.current_routine_index.keys())
            if self.fsm.checkAllServoCompleted(*current_indexes):

                random_index = random.randint(0, len(self.routines) - 1)
                while self.current_routine_index == random_index:
                    random_index = random.randint(0, len(self.routines) - 1)
                self.current_routine_index = random_index
                self.fsm.moveMultipleServo(self.routines[self.current_routine_index])

        # EYE ROUTINE (TODO)

        # AUDIO ROUTINE (TODO)

        # CHANGE STATE

        self.isFirst = False

        if self.fsm.proximity_distance is not None:
            if self.fsm.proximity_distance < 100:
                self.fsm.current_state = 'voting'
                self.isFirst = True
