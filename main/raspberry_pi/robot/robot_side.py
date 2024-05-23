from pathlib import Path

from components.arduino import Arduino
from robot.arm import Arm
from robot.eye import Eye
from robot.mouth import Mouth
from robot.neck import Neck
from robot.side import Side


class RobotSide:
    side: Side
    arduino: Arduino
    eye: Eye
    arm: Arm
    mouth: Mouth
    neck: Neck

    def __init__(self, side: Side, arduino_port: Path, eye: dict, arm: dict, mouth: dict, neck: dict):
        self.side = side
        self.arduino = Arduino(arduino_port)
        self.eye = Eye(**eye)
        self.arm = Arm(self.arduino, **arm)
        self.mouth = Mouth(self.side, self.arduino, **mouth)
        self.neck = Neck(self.arduino, **neck)

    def is_finished(self):
        return self.arduino.is_finished()
