from serial import Serial
from time import sleep

class SerialCommunication:
    port: str
    baudrate: int = 9600
    device: Serial
    
    def __init__(self, port: str, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.device = Serial(port, baudrate, timeout=.1)

    def write(self, data: str):
        self.device.write(bytes(data, 'utf-8'))
        
    def read(self):
        return self.device.readline().decode().strip()
