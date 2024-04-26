from .arduino import Arduino
from time import sleep


class Servo:
    arduino: Arduino
    index: int
    
    
    def __init__(self, arduino: Arduino, index: int):
        self.arduino = arduino
        self.index = index
        
    def move(self, angle: int, speed: int):
        self.arduino.write(f'0 {self.index} 1 {angle} 0 {speed}')
        
    def hi(self):
        self.arduino.write(f'0 {self.index} 5 105 0 95 80 1 100 130 1 100 105 1 100 0 1 95')
        sleep(5)
