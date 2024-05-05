/*
 This function serves as a serial command handler. 
 Serial command arguments **must** be separated by a **space** in the following order:

 * 1. Command number: 0 , 1 or 2.
 *
 *    - 0: Add new movements to a servo motor. If this is the command chosed, the following should be:  
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
 *    - 1: Inquire whether the servo motor has finished its execution (return 1 if the movements are completed, 0 if not). If this is the command chosed the following should be: 
 *
 *          2. Servo number: From 0 to the total number of servos minus 1. (Servos are meant to be connected in consecutive pins)
 *
 *    Example of input: 1 2 -> Inquire if the Servo no 2 has finished or not
        
 *    - 2: Add new movements to a steeper motor controlling the displacement wrt the origin of an axis by a gear . If this is the command chosed, the following should be:  
 *            
 *          2. Stepper number: From 0 to the total number of stepper minus 1. (Stepper are meant to be connected in consecutive pins)
 * 
 *          3. Percentage (integer value) of displacent of the axis (0 if is at the origin, 100 is it is at maximum displacement wrt the origin).
 * 
 *          4. Velocity of the gear (MIN SPEED 15, MAX SPEED 30)
 * 
 *          5. Lenght of the bouncing that the axis start to do after reaching the wanted displacement in millimeters (0 for no bouncing) (if this value is greather then MAX_BOUNCING = 0.5 centimeter is saturate at this value)
 * 
 *          6. Velocity of the gear for the bouncing (MIN SPEED 15, MAX SPEED 30)
 *    
 *    Example of input: 2 0 90 20 10 30 -> This command cause the Stepper no 0 to move the axis to 90% of maximum displacement moving the gear at 15 speed , then after reaching the displacemnt it start bouncing up and down of 2 centimeters with gear speed of 30
 *   
 */

#include <Arduino.h>
#include "stepper_controller.h"
#define MAX_COMMAND_LENGTH 400

unsigned long currentMillis;
int command[MAX_COMMAND_LENGTH];

void setup() {
  Serial.begin(9600);
  initializeSteppers();
}

void loop() {
  currentMillis = millis();

  if (Serial.available() > 0) {
    int commandIndex = 0;

    while (Serial.available() > 0) {
      command[commandIndex] = Serial.parseInt();
      commandIndex++;
    }

    if (command[0] == 2) {
      int i = 1;
      int totStepper = command[i++];
      for(int stepper = 0; stepper < totStepper; stepper++){
        addMovementStepper(command[i], command[i+1] , command[i+2], command[i+3] , command[i+4] ,currentMillis);
        i = i + 5;
      }
    }
  }

  updateSteppers(currentMillis);
}