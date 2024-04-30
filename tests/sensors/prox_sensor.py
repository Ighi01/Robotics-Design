import time
import board
import adafruit_hcsr04
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D20, echo_pin=board.D21)

while True:
    try:
        print(round(sonar.distance))
    except RuntimeError as e:
        print(e)
    time.sleep(0.1)
