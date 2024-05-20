from pathlib import Path
from time import time_ns, sleep

from serial import Serial

from components.curve import Curve

servo_template_main: str = '0 {servo_len} {servos}'
servo_template_ind: str = '{index} {movnum} {movs}'
servo_template_mov: str = '{angle} {delay} {velocity} {curve}'
check_template: str = '1 {servo_len} {servos}'
check_template_all: str = '1 0'
reset_template: str = '2 {servo_len} {servos}'
reset_template_all: str = '2 0'
stepper_template: str = '3 {percentage} {velocity} {bounce_distance} {bounce_velocity}'


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
        while self.read() != 'ack':
            sleep(0.1)
        self.write('connect')
        print(f'Arduino in port {port} connected')

    def write(self, data: str):
        while time_ns() - self.last_sent < 1000000:
            pass
        self.device.write(bytes(data, 'utf-8'))
        self.last_sent = time_ns()

    def read(self):
        return self.device.readline().decode().strip()

    def add_servo_movement(self, index: int, angle: int, delay: int, velocity: int, curve: Curve):
        if index not in self.servo_movements:
            self.servo_movements[index] = []
        self.servo_movements[index].append((angle, delay, velocity, curve))

    def send_servo_movements(self):
        servos = []
        for index, movements in self.servo_movements.items():
            movs = []
            for angle, delay, velocity, curve in movements:
                movs.append(servo_template_mov.format(
                    angle=angle,
                    delay=delay,
                    velocity=velocity,
                    curve=curve.value
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
        
    def is_finished(self, indexes: list[int] = []) -> bool:
        if not indexes:
            self.write(check_template_all)
        else:
            self.write(check_template.format(
                servo_len=len(indexes),
                servos=' '.join(map(str, indexes))
            ))
        while True:
            response = self.read()
            if response == '':
                continue
            return response == '1'

    def reset(self, indexes: list[int] = []):
        if not indexes:
            self.write(reset_template_all)
        else:
            self.write(reset_template.format(
                servo_len=len(indexes),
                servos=' '.join(map(str, indexes))
            ))

    def move_stepper(self, percentage, velocity, bounce_distance, bounce_velocity):
        self.write(stepper_template.format(
            percentage=percentage,
            velocity=velocity,
            bounce_distance=bounce_distance,
            bounce_velocity=bounce_velocity
        ))
