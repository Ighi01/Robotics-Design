import RPi.GPIO as IO
from time import sleep

pin = 16

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(pin,IO.IN)

def callback(_):
    print('IR sensor detected something')

IO.add_event_detect(pin, IO.FALLING, callback=callback, bouncetime=200)

while True:
    pass