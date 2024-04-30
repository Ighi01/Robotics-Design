import RPi.GPIO as IO
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(3,IO.IN)

def callback(_):
    print('IR sensor detected something')

IO.add_event_detect(3,IO.FALLING, callback=callback, bouncetime=200)

while True:
    pass