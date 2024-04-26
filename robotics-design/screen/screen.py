from time import sleep
from adafruit_rgb_display.st7735 import ST7735R
from threading import Thread
from digitalio import DigitalInOut
import board
from PIL import Image, ImageDraw, ImageSequence

spi = board.SPI()

class Screen:
    device: ST7735R
    current_thread: Thread
    stop: bool = False
    
    def __init__(cls, cs: DigitalInOut, dc: DigitalInOut, rst: DigitalInOut):
        cls.device = ST7735R(
            spi, 
            rotation=0,
            cs=cs,
            dc=dc,
            rst=rst,
            baudrate=24000000,
            bgr=True
        )
        cls.current_thread = None
        
    def _stop(self):
        self.stop = True
        if self.current_thread:
            self.current_thread.join()
        self.stop = False
        
    def _blank(self):
        if self.device.rotation % 180 == 90:
            height = self.device.width  # we swap height/width to rotate it to landscape!
            width = self.device.height
        else:
            width = self.device.width  # we swap height/width to rotate it to landscape!
            height = self.device.height
        image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        self.device.image(image)
        
    def blank(self):
        self._stop()
        self.current_thread = Thread(target=self._blank)
        self.current_thread.start()
        
    def _gif(self, path):
        images = []
        with Image.open(path) as im:
            for frame in ImageSequence.Iterator(im):
                frame = frame.convert('RGB')
                images.append(frame)
        while not self.stop:
            for frame in images:
                self.device.image(frame)
                
    def gif(self, path):
        self._stop()
        self.current_thread = Thread(target=self._gif, args=(path,))
        self.current_thread.start()
