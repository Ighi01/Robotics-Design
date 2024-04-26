#include <Arduino.h>
#include "servo_controller.h"
#define MAX_COMMAND_LENGTH 140
#define MAX_SERVO 11
#define INITIAL_PIN_SERVOS 2

/*
 This function serves as a serial command handler. 
 Serial command arguments **must** be separated by a **space** in the following order:

 * 1. Command number: 0 or 1.
 *
 *    - 0: Add new movements to a servo. If this is the command chosed, the following should be:  
 *            
 *          2. Servo number: From 0 to the total number of servos minus 1. (Servos are meant to be connected in consecutive pins)
 * 
 *          3. Number of movements to assign to the servo (0 to 20).
 * 
 *          4. For each movement assigned to the servo:
 *                  - Angle to assign to the servo (in degrees, must be integer).
 *                  - Delay after the previous movement to start the movement (in seconds). Use 0 for immediate movement.
 *                  - Movement speed in degrees per second . Use 100 for instant transition.
 *              NOTE: The number of movements specified must match the number of triplets provided. All those arguments must be separated by space ,too
 *    
 *    Example of input: 0 0 2 90 0 90 0 5 100 -> This command cause the Servo no 0 to move to 90 degrees immediatelly (since 0 delay) at 90 deg/sec velocity and then after 5 seconds from the prevoius movement move to 0 degrees instantly (since 100 velocity), then finish
 *    
 *    - 1: Inquire whether the servo has finished its execution (return 1 if the movements are completed, 0 if not). If this is the command chosed the following should be: 
 *
 *          2. Servo number: From 0 to the total number of servos minus 1. (Servos are meant to be connected in consecutive pins)
 *
 *    Example of input: 1 2 -> Inquire if the Servo no 2 has finished or not
 *
 */

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