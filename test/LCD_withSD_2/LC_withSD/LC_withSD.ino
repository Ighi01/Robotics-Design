#include <Adafruit_ST7735.h>
#include <SPI.h>
#include <SD.h>

#define TFT_CS  10  // Chip select line for TFT display
#define TFT_RST  8  // Reset line for TFT (or see below...)
#define TFT_DC   9  // Data/command line for TFT
#define SD_CS    4  // Chip select line for SD card

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

void setup() {
  Serial.begin(9600);

  tft.initR(INITR_BLACKTAB);

  Serial.print("Initializing SD card...");
  if (!SD.begin(SD_CS)) {
    Serial.println("failed!");
    return;
  }
  Serial.println("OK!");

  tft.setRotation(1); // Landscape
}

void loop() {
  char* filenames[] = {"img1.bmp", "img2.bmp", "img3.bmp", "img4.bmp", "img5.bmp", "img6.bmp"};
  for (int i = 0; i < sizeof(filenames) / sizeof(filenames[0]); i++) {
    bmpDraw(filenames[i], 0, 0);
    delay(1000); // Adjust delay if necessary
  }
}

#define BUFFPIXEL 80
#define READBUFFERSIZE 1024 // Adjust buffer size if necessary

void bmpDraw(char* filename, uint8_t x, uint8_t y) {
  File bmpFile = SD.open(filename);
  if (!bmpFile) {
    Serial.print("Error opening file: ");
    Serial.println(filename);
    return;
  }

  uint8_t buffer[READBUFFERSIZE];
  uint16_t bytesRead;

  // Read BMP header
  bmpFile.seek(18); // Jump to width and height bytes
  uint16_t bmpWidth = bmpFile.read() | (bmpFile.read() << 8);
  uint16_t bmpHeight = bmpFile.read() | (bmpFile.read() << 8);
  bmpFile.seek(54); // Jump to pixel data

  Serial.print("Width: ");
  Serial.println(bmpWidth);
  Serial.print("Height: ");
  Serial.println(bmpHeight);

  // Calculate row size
  uint32_t rowSize = (bmpWidth * 3 + 3) & ~3;

  // Set TFT address window
  tft.setAddrWindow(x, y, x + bmpWidth - 1, y + bmpHeight - 1);

  for (uint16_t row = 0; row < bmpHeight; row++) {
    bytesRead = bmpFile.readBytes(buffer, min(READBUFFERSIZE, rowSize));
    if (bytesRead <= 0) break;

    for (uint16_t col = 0; col < bytesRead; col += 3) {
      uint16_t color = tft.color565(buffer[col + 2], buffer[col + 1], buffer[col]);
      tft.pushColor(color);
    }
  }

  bmpFile.close();
}
