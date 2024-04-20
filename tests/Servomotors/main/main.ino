#include <Arduino.h>
#include "servo_controller.h"
#define MAX_COMMAND_LENGTH 140
#define MAX_SERVO 11
#define INITIAL_PIN_SERVOS 2

unsigned long currentMillis;
int servoIndex;
int totMovement;
int i,j;
int command[MAX_COMMAND_LENGTH];

void setup() {
  Serial.begin(9600);
  initializeServos(MAX_SERVO, INITIAL_PIN_SERVOS);
}

void loop() {
  currentMillis = millis();

  if (Serial.available() > 0) {
    int commandIndex = 0;

    while (Serial.available() > 0) {
      command[commandIndex] = Serial.parseInt();
      commandIndex++;
    }

    if (command[0] == 0) {
      servoIndex = command[1];
      totMovement = command[2];
      Movement path[totMovement];
      i = 3;
      j = 0;
      while (i < 3*(totMovement+1)) {
        path[j].ang = command[i++];
        path[j].del = command[i++];
        path[j++].speed = command[i++];
      }
      addMovement(servoIndex, path, totMovement, currentMillis);
    }

    if (command[0] == 1) {
      servoIndex = command[1];
      Serial.println(isComplete(servoIndex));
    }
  }

  updateServos(currentMillis);
  delay(10);
}