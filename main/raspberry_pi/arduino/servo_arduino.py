from arduino.arduino import Arduino


class ServoArduino(Arduino):
    def add_movement(self, servo: int, angle: int, delay: int, speed: int):
        if servo not in self.movements:
            self.movements[servo] = []
        self.movements[servo].append((angle, delay, speed))

    def move(self):
        command = '0'
        for servo, movements in self.movements.items():
            command += f" {servo} {len(movements)}"
            for angle, delay, speed in movements:
                command += f" {angle} {delay} {speed}"
        self.write(command)

    def erase(self):
        self.movements.clear()

    def move_instantly(self, servo: int, angle: int, delay: int, speed: int):
        command = f"0 1 {servo} 1 {angle} {delay} {speed}"
        self.write(command)
