#include <SPI.h>
#include <SD.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>

#define TFT_CS     10
#define TFT_RST    9
#define TFT_DC     8

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

void setup() {
  Serial.begin(9600);
  
  // Initialize SD card
  if (!SD.begin(TFT_CS)) {
    Serial.println("SD card initialization failed!");
    return;
  }
  
  // Initialize TFT display
  tft.initR(INITR_BLACKTAB); // Initialize ST7735 with black tab

  // Read and display the three images
  displayImage("image1.bmp", 0, 0);
  displayImage("image2.bmp", 0, 80); // Assuming each image is 80 pixels in height
  displayImage("image3.bmp", 0, 160); // Assuming each image is 80 pixels in height
}

void loop() {
  // Nothing to do here
}

void displayImage(const char* filename, int16_t x, int16_t y) {
  File file = SD.open(filename);
  if (!file) {
    Serial.print("Failed to open file: ");
    Serial.println(filename);
    return;
  }

  if (!bmpDraw(&file, x, y)) {
    Serial.println("BMP image rendering failed");
  }

  file.close();
}

#define BUFFPIXEL 20

// This function will draw a bitmap image loaded from the SD card
bool bmpDraw(File *bmpFile, int16_t x, int16_t y) {
  uint32_t seekOffset;
  uint16_t w, h;
  uint8_t  bmpDepth, padding;
  uint32_t rowSize;

  // Parse BMP header
  if (read16(bmpFile) == 0x4D42) { // BMP signature
    seekOffset = read32(bmpFile);
    read32(bmpFile); // Read & ignore creator bytes
    seekOffset += read32(bmpFile); // Start of image data

    // Read DIB header
    read32(bmpFile); // Read & ignore header size
    w = read32(bmpFile);
    h = read32(bmpFile);
    if (read16(bmpFile) == 1) { // # planes -- must be '1'
      bmpDepth = read16(bmpFile); // bits per pixel
      if ((bmpDepth == 24) && (read32(bmpFile) == 0)) { // 0 = uncompressed
        padding = (4 - ((w * 3) % 4)) % 4; // Padding bytes at end of each row
        rowSize = (w * 3 + padding); // Size of each row in bytes

        // Start drawing
        uint8_t  sdbuffer[BUFFPIXEL * 3]; // 3 bytes per pixel
        for (int32_t row = 0; row < h; row++) { // For each scanline...
          // Seek to start of scan line
          bmpFile->seek(seekOffset + (rowSize * row));
          for (uint32_t col = 0; col < w; col++) { // For each pixel...
            bmpFile->read(sdbuffer, 3); // Read 3 bytes (RGB) per pixel

            // Convert pixel from BMP to TFT format, push to display
            uint16_t color = tft.color565(sdbuffer[2], sdbuffer[1], sdbuffer[0]);
            tft.drawPixel(x + col, y + row, color);
          } // end pixel
        } // end scanline
        return true; // Success
      } // end good BMP
    }
  }

  Serial.println(F("Not a BMP"));
  return false; // Failure
}

// Helper function to read little endian 16-bit integers from file
uint16_t read16(File *f) {
  uint16_t result;
  ((uint8_t *)&result)[0] = f->read(); // LSB
  ((uint8_t *)&result)[1] = f->read(); // MSB
  return result;
}

// Helper function to read little endian 32-bit integers from file
uint32_t read32(File *f) {
  uint32_t result;
  ((uint8_t *)&result)[0] = f->read(); // LSB
  ((uint8_t *)&result)[1] = f->read();
  ((uint8_t *)&result)[2] = f->read();
  ((uint8_t *)&result)[3] = f->read(); // MSB
  return result;
}



