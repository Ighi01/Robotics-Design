from pathlib import Path
from time import time_ns, sleep

from serial import Serial

from components.curve import Curve

servo_template_main: str = '0 {servo_len} {servos}'
servo_template_ind: str = '{index} {movnum} {movs}'
servo_template_mov: str = '{angle} {delay} {velocity} {curve}'
reset_template: str = '{len} 1 {servo_len} {servos}'
reset_template_all: str = '2 1 0'
stepper_template: str = '2 {percentage} {velocity} {bounce_distance} {bounce_velocity}'


class Arduino:
    port: Path
    baudrate: int = 9600
    device: Serial
    last_sent: int = 0
    servo_movements: dict[int, list[tuple[int, int, int, Curve]]]

    def __init__(self, port: Path, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.servo_movements = {}
    
    def connect(self):
        self.device = Serial(str(self.port), self.baudrate)
        while self.read() != 'ack':
            sleep(0.1)
        self.write('a')
        sleep(0.1)
        print(f'Arduino in port {self.port} connected')
        

    def write(self, data: str):
        while time_ns() - self.last_sent < 10000000:
            pass
        self.device.write(bytes(data, 'utf-8'))
        self.last_sent = time_ns()

    def read(self):
        a = self.device.readline().decode().strip()
        return a

    def add_servo_movement(self, index: int, angle: int, delay: int, velocity: int, curve: Curve):
        if index not in self.servo_movements:
            self.servo_movements[index] = []
        self.servo_movements[index].append((angle, delay, velocity, curve))

    def send_servo_movements(self):
        print(self.servo_movements)
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
        command = servo_template_main.format(servo_len=len(servos), servos=' '.join(servos))
        command_list = command.split(' ')
        command_list = [str(len(command_list))] + command_list
        command_split = [command_list[i:i + 15] for i in range(0, len(command_list), 15)]
        for command in command_split:
            print(' '.join(command))
            self.write(' ' + ' '.join(command) + ' ')
        self.servo_movements = {}
    
    def wait_servos(self):
        while self.read() != 'ok':
            sleep(0.1)

    def reset(self, indexes: list[int] = []):
        if not indexes:
            self.write(reset_template_all)
        else:
            self.write(reset_template.format(
                len=len(indexes) + 2,
                servo_len=len(indexes),
                servos=' '.join(map(str, indexes))
            ))

    def move_stepper(self, percentage, velocity, bounce_distance, bounce_velocity):
        self.write('5 ' + stepper_template.format(
            percentage=percentage,
            velocity=velocity,
            bounce_distance=bounce_distance,
            bounce_velocity=bounce_velocity
        ))

    def wait_stepper(self):
        while self.read() != 'ko':
            sleep(0.1)

    def wait(self):
        servos_done = False
        stepper_down = False
        while not servos_done or not stepper_down:
            res = self.read()
            if res == 'ok':
                servos_done = True
            if res == 'ko':
                stepper_down = True
            sleep(0.1)
