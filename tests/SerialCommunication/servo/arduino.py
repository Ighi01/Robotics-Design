from serial import Serial
from time import sleep

class Arduino:
    port: str
    baudrate: int = 9600
    device: Serial
    
    def __init__(self, port: str, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.device = Serial(port, baudrate, timeout=.1)

    def write(self, data: str):
        self.device.write(bytes(data, 'utf-8'))
        
    def wait_until_finished(self, motor):
        while True:
            self.device.write(f'1 {motor}'.encode())
            sleep(.05)
            print(self.device.readline().decode())
            if self.device.readline().decode() == '1':
                break
            else:
                sleep(.2)
