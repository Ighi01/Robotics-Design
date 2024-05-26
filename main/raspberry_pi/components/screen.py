from time import sleep
from adafruit_rgb_display.st7735 import ST7735R
import threading
from digitalio import DigitalInOut
import board
from PIL import Image, ImageDraw, ImageSequence

spi = board.SPI()


def custom_hook(args):
    # report the failure
    print(f'Thread failed: {args.exc_value}')


threading.excepthook = custom_hook


class Screen:
    device: ST7735R
    thread: threading.Thread
    blank_image: Image
    images: list
    change: bool
    
    def _loop(self):
        while True:
            self.change = False
            for frame in self.images:
                if self.change:
                    break
                self.device.image(frame)
    
    def __init__(self, cs: DigitalInOut, dc: DigitalInOut, rst: DigitalInOut):
        self.device = ST7735R(
            spi, 
            rotation=0,
            cs=cs,
            dc=dc,
            rst=rst,
            baudrate=24000000,
            bgr=True
        )
        if self.device.rotation % 180 == 90:
            height = self.device.width
            width = self.device.height
        else:
            width = self.device.width
            height = self.device.height
        self.blank_image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(self.blank_image)
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        self.images = [self.blank_image]
        self.thread = threading.Thread(target=self._loop)
        self.thread.start()
        self.change = False
    
    def blank(self):
        self.images = [self.blank_image]

    def gif(self, path):
        frames = []
        with Image.open(path) as im:
            for frame in ImageSequence.Iterator(im):
                frame = frame.convert('RGB')
                frames.append(frame)
        self.images = frames
        self.change = True
