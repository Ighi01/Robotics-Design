from arduino.arduino import Arduino


class StepperArduino(Arduino):
    movements: dict[int, tuple]

    def add_movement(self, stepper: int, percentage: int, velocity: int, bouncing_length: int, bouncing_velocity: int):
        self.movements[stepper] = (percentage, velocity, bouncing_length, bouncing_velocity)

    def move(self):
        command = '2'
        command += f" {len(self.movements)}"
        for stepper, movements in self.movements.items():
            command += f" {stepper} {' '.join(map(str, movements))}"
        self.write(command)

    def erase(self):
        self.movements.clear()

    def move_instantly(self, stepper: int, percentage: int, velocity: int, bouncing_length: int, bouncing_velocity: int):
        command = f"2 1 {stepper} {percentage} {velocity} {bouncing_length} {bouncing_velocity}"
        self.write(command)
