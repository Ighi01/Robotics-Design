import digitalio
import board
from PIL import Image, ImageDraw, ImageSequence
from adafruit_rgb_display import st7735

spi = board.SPI()

ls = st7735.ST7735R(
    spi, 
    rotation=0,
    cs=digitalio.DigitalInOut(board.CE0),
    dc=digitalio.DigitalInOut(board.D25),
    rst=digitalio.DigitalInOut(board.D24),
    baudrate=24000000,
    bgr=True
)

rs = st7735.ST7735R(
    spi, 
    rotation=0,
    cs=digitalio.DigitalInOut(board.CE1),
    dc=digitalio.DigitalInOut(board.D6),
    rst=digitalio.DigitalInOut(board.D5),
    baudrate=24000000,
    bgr=True
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if rs.rotation % 180 == 90:
    height = rs.width  # we swap height/width to rotate it to landscape!
    width = rs.height
else:
    width = rs.width  # we swap height/width to rotate it to landscape!
    height = rs.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
rs.image(image)
ls.image(image)

images = []
with Image.open('sad.gif') as im:
    for frame in ImageSequence.Iterator(im):
        frame = frame.convert('RGB')
        images.append(frame)
        
while True:
    for frame in images:
        ls.image(frame)
        rs.image(frame)
