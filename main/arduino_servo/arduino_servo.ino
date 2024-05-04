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
 *          4. Velocity of the gear (rpm)
 * 
 *          5. Lenght of the bouncing that the axis start to do after reaching the wanted displacement in centimeters (0 for no bouncing) (if this value is greather then MAX_BOUNCING is saturate at this value)
 * 
 *          6. Velocity of the gear for the bouncing (rpm)
 *    
 *    Example of input: 2 1 90 100 2 200 -> This command cause the Stepper no 1 to move the axis to 90% of maximum displacement moving the gear at 100 rpm , then after reaching the displacemnt it start bouncing up and down of 2 centimeters with gear speed of 200 rpm
 *    
 */

#include <Arduino.h>
#include "servo_controller.h"
#define MAX_COMMAND_LENGTH 400

unsigned long currentMillis;
int command[MAX_COMMAND_LENGTH];

void setup() {
  Serial.begin(9600);
  //Serial.println("ciao");
  initializeServos();
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
      int i = 1;
      int totServo = command[i++];

      for(int servo = 0; servo < totServo; servo ++){
        int servoIndex = command[i++];
        int totMovement = command[i++];
        Movement path[totMovement];
        int h = i;
        int j = 0;
        while (i < (3*totMovement + h)) {
          path[j].ang = command[i++];
          path[j].del = command[i++];
          path[j++].speed = command[i++];
        }
        addMovementServo(servoIndex, path, totMovement, currentMillis);
      }
    }

    if (command[0] == 1) {
      int i = 1;
      int totServo = command[i++];
      int result = true;
      while(i< (totServo + 1)){
        if(!isCompleteServo(command[i++])){
          result = false;
          break;
        }
      }
      Serial.println(result);
    }
  }

  updateServos(currentMillis);
  delay(10);
}