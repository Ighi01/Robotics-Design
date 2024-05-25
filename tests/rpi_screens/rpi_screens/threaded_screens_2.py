from time import sleep
from adafruit_rgb_display.st7735 import ST7735R
from threading import Thread
from digitalio import DigitalInOut
import board
from PIL import Image, ImageDraw, ImageSequence

spi = board.SPI()


class Screen:
    device: ST7735R
    thread: Thread
    blank_image: Image
    images: list
    
    def _loop(self):
        while True:
            for frame in self.images:
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
        self.thread = Thread(target=self._loop)
        self.thread.start()
    
    def blank(self):
        self.images = [self.blank_image]
        
    def sad(self):
        frames = []
        with Image.open('sad-green.gif') as im:
            for frame in ImageSequence.Iterator(im):
                frame = frame.convert('RGB')
                frames.append(frame)
        self.images = frames
        
    def happy(self):
        frames = []
        with Image.open('happy1-orange.gif') as im:
            for frame in ImageSequence.Iterator(im):
                frame = frame.convert('RGB')
                frames.append(frame)
        self.images = frames
        
        

if __name__ == '__main__':
    left_screen = Screen(DigitalInOut(board.D17), DigitalInOut(board.D25), DigitalInOut(board.D24))
    right_screen = Screen(DigitalInOut(board.D27), DigitalInOut(board.D6), DigitalInOut(board.D5))
    
    print('Blanking screens')
    left_screen.blank()
    right_screen.blank()
    
    sleep(2)
    
    print('Showing sad face')
    left_screen.happy()
    right_screen.sad()
    
    sleep(5)
    
    print('Blanking screens')
    left_screen.blank()
    right_screen.blank()
