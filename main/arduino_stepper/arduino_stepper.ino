/*
  This function serves as a serial command handler for controlling multiple stepper motor simultaneously. 
  Serial command arguments **must** be separated by a **space** in the following order:        
 *          
 * 1. Number of Stepper: From 1 to the total number of stepper. For each stepper that you want to move you must specify those commands:
 * 
 *       2. Stepper number: From 0 to the total number of stepper minus 1. (Stepper are meant to be connected in consecutive pins)
 * 
 *       3. Percentage (integer value) of displacent of the axis (0 if is at the origin, 100 is it is at maximum displacement wrt the origin)
 * 
 *       4. Velocity of the gear (MIN SPEED 15, MAX SPEED 30)
 * 
 *       5. Lenght of the bouncing that the axis start to do after reaching the wanted displacement in millimeters (0 for no bouncing) (if this value is greather then MAX_BOUNCING = 0.5 centimeter is saturate at this value)
 * 
 *       6. Velocity of the gear for the bouncing (MIN SPEED 15, MAX SPEED 30)
 * 
 * NOTE: The number of stepper specified must match the number of stepper then provided. All those arguments must be separated by space ,too
 *
 * Example of input: 2 0 90 20 5 30 1 10 30 3 20 -> This command cause 2 stepper to move simultaneously: the Stepper no 0 to move the axis to 90% of maximum displacement moving the gear at 20 speed , then after reaching the displacemnt it start bouncing up and down of 5 millimiterss with gear speed of 30;
 *                                                                                                            in parallel it also cause the Stepper no 1 to move the axis to 10% of maximum displacement moving the gear at 30 speed , then after reaching the displacemnt it start bouncing up and down of 3 millimiterss with gear speed of 20
 */

#include <Arduino.h>
#include "stepper_controller.h"
#define MAX_COMMAND_LENGTH 400

unsigned long currentMillis;
int command[MAX_COMMAND_LENGTH];

void setup() {
  Serial.begin(9600);
  initializeSteppers();
  while (Serial.available() <= 0) {
    Serial.println("ack");
    delay(1000);
  }
}

void loop() {
  currentMillis = millis();

  if (Serial.available() > 0) {
    int commandIndex = 0;

    while (Serial.available() > 0) {
      command[commandIndex] = Serial.parseInt();
      commandIndex++;
    }

    int i = 0;
    int totStepper = command[i++];
    for(int stepper = 0; stepper < totStepper; stepper++){
      addMovementStepper(command[i], command[i+1] , command[i+2], command[i+3] , command[i+4] ,currentMillis);
      i = i + 5;
    }
  }

  updateSteppers(currentMillis);
}