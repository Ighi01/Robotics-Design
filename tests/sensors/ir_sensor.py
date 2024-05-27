#!/home/dietpi/.cache/pypoetry/virtualenvs/sensors-ZBOxR5Ay-py3.11/bin/python

import RPi.GPIO as IO
from time import sleep

pin = 19

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(pin,IO.IN)

def callback(_):
    print('IR sensor detected something')

IO.add_event_detect(pin, IO.FALLING, callback=callback, bouncetime=200)

while True:
    pass
