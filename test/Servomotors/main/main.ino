#include <Arduino.h>
#include "servo_controller.h"

const int SERVOS = 2;
const int INITIAL_PIN_SERVOS = 6;
const unsigned long intervalUpdate = 10;
const unsigned long angleIncrement = 1; //NOTE: angle % increment == 0 !

const int mouthPin = 6;
const int armPin = 7;

const int irPin = 8;
const long irInterval = 100;
unsigned long irPreviousMillis = 0;
bool irValue, irOldValue;

unsigned long currentMillis;

void setup() {
  initializeServos(SERVOS,INITIAL_PIN_SERVOS,intervalUpdate,angleIncrement);
  pinMode(irPin, INPUT);
  
  int movementsServo0[3] = {0, 10, 90}; // Array dei movimenti per il servo 0
  int delaysServo0[3] = {0, 3, 5};      // Array dei ritardi per il servo 0
  addMovement(0, 3, movementsServo0, delaysServo0);

  int movementsServo1[3] = {45, 60, 80}; // Array dei movimenti per il servo 1
  int delaysServo1[3] = {0, 2, 4};        // Array dei ritardi per il servo 1

  addMovement(1, 3, movementsServo1, delaysServo1);
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

  updateServos(currentMillis);
}



