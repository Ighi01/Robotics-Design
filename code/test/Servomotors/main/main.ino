#include <Arduino.h>
#include "servo_controller.h"

const int SERVOS = 2;
const int INITIAL_PIN_SERVOS = 6;
const int mouthPin = 6;
const int armPin = 7;

const int irPin = 8;
const long irInterval = 100;
unsigned long irPreviousMillis = 0;
bool irValue, irOldValue;

unsigned long currentMillis;

void setup() {
  Serial.begin(9600);
  initializeServos(SERVOS,INITIAL_PIN_SERVOS);
  pinMode(irPin, INPUT);
  
  int movementsServo0[6] = {0, 50, -90, 10 , -30 ,0}; // Array dei movimenti per il servo 0
  int delaysServo0[6] = {0, 25, 10, 15, 40, 25};      // Array dei ritardi per il servo 0
  int velocitiesServo0[6] = {90, 45, 10, 180, 270, 45};      // Array dei ritardi per il servo 0

  addMovement(0, 6, movementsServo0, delaysServo0, velocitiesServo0);

  int movementsServo1[6] = {0, 60, -90, -10 , 80 ,0}; // Array dei movimenti per il servo 1
  int delaysServo1[6] = {0, 15, 10, 15, 30, 25};        // Array dei ritardi per il servo 1
  int velocitiesServo1[6] = {90, 45, 10, 180, 270, 45};      // Array dei ritardi per il servo 0

  addMovement(1, 6, movementsServo1, delaysServo1, velocitiesServo1);
}

void loop() {
  currentMillis = millis();

  if (currentMillis - irPreviousMillis >= irInterval) {
    irPreviousMillis = currentMillis;
    irValue = digitalRead(irPin);
    
    if (!irValue && irOldValue) {
      //setDelayedPosition(0, 45, 5000);
      //setDelayedPosition(1, 90, 5000);
    }

    irOldValue = irValue;
  }

  static unsigned long printPreviousMillis = 0;
  if (currentMillis - printPreviousMillis >= 10000) {
    printPreviousMillis = currentMillis;
    
    Serial.println(currentMillis/1000);
    printServoData();
    
  }

  updateServos(currentMillis);
  updateAngles(currentMillis);
  delay(10);
}



