class Servo:
    arduino: Arduino
    index: int
    
    def __init__(self, arduino: Arduino, index: int):
        self.arduino = arduino
        self.index = index
        
    def move(self, angles: list, delays: list, speeds: list):
        if len(angles) != len(delays) or len(delays) != len(speeds):
            raise ValueError("The lengths of angles, delays, and speeds must be equal")
        
        movements = [f"{angles[i]} {delays[i]} {speeds[i]}" for i in range(len(angles))]
        command = f"0 {self.index} {len(angles)} {' '.join(movements)}"
        self.arduino.write(command)
        
    def is_completed(self):
        command = f"1 {self.index}"
        self.arduino.write(command)
        response = self.arduino.read()
        return bool(int(response))
    
    def wait_until_finished(self):     # Stare attenti quando si stalla la CPU dentro un "while true" , piu' prudente farlo da un thread
        while not self.is_completed():
            sleep(0.2)
