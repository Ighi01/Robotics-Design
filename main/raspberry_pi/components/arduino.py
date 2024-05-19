from pathlib import Path
from time import time_ns

from serial import Serial

servo_template_main: str = '0 {servo_len} {servos}'
servo_template_ind: str = '{index} {movnum} {movs}'
servo_template_mov: str = '{angle} {delay} {velocity}'
stepper_template: str = '2 {percentage} {velocity} {bounce_distance} {bounce_velocity}'


class Arduino:
    port: Path
    baudrate: int = 9600
    device: Serial
    last_sent: int = 0
    servo_movements: dict[int, list[tuple[int, int, int]]] = {}

    def __init__(self, port: Path, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.device = Serial(str(port), baudrate, timeout=.1)

    def write(self, data: str):
        while time_ns() - self.last_sent < 1000000:
            pass
        self.device.write(bytes(data, 'utf-8'))
        self.last_sent = time_ns()

    def read(self):
        return self.device.readline().decode().strip()

    def move_stepper(self, percentage, velocity, bounce_distance, bounce_velocity):
        self.write(stepper_template.format(
            percentage=percentage,
            velocity=velocity,
            bounce_distance=bounce_distance,
            bounce_velocity=bounce_velocity
        ))

    def add_servo_movement(self, index: int, angle: int, delay: int, velocity: int):
        if index not in self.servo_movements:
            self.servo_movements[index] = []
        self.servo_movements[index].append((angle, delay, velocity))

    def send_servo_movements(self):
        servos = []
        for index, movements in self.servo_movements.items():
            movs = []
            for angle, delay, velocity in movements:
                movs.append(servo_template_mov.format(
                    angle=angle,
                    delay=delay,
                    velocity=velocity
                ))
            servos.append(servo_template_ind.format(
                index=index,
                movnum=len(movs),
                movs=' '.join(movs)
            ))
        self.write(servo_template_main.format(
            servo_len=len(servos),
            servos=' '.join(servos)
        ))
        self.servo_movements = {}
