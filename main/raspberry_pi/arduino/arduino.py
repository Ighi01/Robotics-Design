from enum import Enum

from serial import Serial


class Mode(Enum):
    SERVO = 0
    STEPPER = 1


class Arduino:
    port: str
    baudrate: int = 9600
    device: Serial
    mode: Mode
    movements: dict[int, list[tuple]]

    def __init__(self, port: str, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.device = Serial(port, baudrate, timeout=.1)

    def write(self, data: str):
        self.device.write(bytes(data, 'utf-8'))

    def read(self):
        return self.device.readline().decode().strip()
