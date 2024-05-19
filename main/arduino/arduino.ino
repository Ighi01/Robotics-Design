/*
  This function serves as a serial command handler for controlling multiple servo motors simultaneously
  Serial command arguments **must** be separated by a **space** in the following order:

 * 1. Command number: 0 or 1.
 *
 *    - 0: Add new movements to the servo motors. If this is the command chosed, the following should be:  
 *           
 *          2. Number of Servo: From 1 to the total number of servos. For each servos that you want to move you must specify those commands:
 *  
 *               3. Servo index: From 0 to the total number of servos minus 1. (Servos are meant to be connected in consecutive pins)
 * 
 *               4. Number of movements to assign to the servo (0 to 20).
 * 
 *               5. For each movement assigned to the servo:
 *                   - Angle to assign to the servo (in degrees, must be integer).
 *                   - Delay after the previous movement to start the movement (in seconds). Use 0 for immediate movement.
 *                   - Movement speed in degrees per second . Use 100 for instant transition.
 *               NOTE: The number of movements specified must match the number of triplets provided. All those arguments must be separated by space ,too
 * 
 *          NOTE: The number of servo specified must match the number of servos then provided. All those arguments must be separated by space ,too
 *
 *      Example of input: 0 2 0 2 90 0 90 0 5 100 3 1 60 0 30 -> This command cause 2 servo to move simultaneously: the Servo no 0 to move to 90 degrees immediatelly (since 0 delay) at 90 deg/sec velocity and then after 5 seconds 
 *                                                           from the prevoius movement move to 0 degrees instantly (since 100 velocity), then finish; 
 *                                                           in parallel it also cause the Servo no3 to move of 60 degrees immediatelly at 30 deg/sec velocity, then finish
 *    0 4 0 4 90 0 75 0 2 100 90 2 75 0 2 100 1 4 90 0 75 0 2 100 90 2 75 0 2 100 3 3 180 0 100 0 4 75 90 3 50 2 2 180 0 90 0 5 50
 *    - 1: Inquire whether the given servo motors are all finished its execution (return 1 if all the movements of all the given servos are completed, 0 if not). If this is the command chosed the following should be: 
 *
 *          2. Number of Servo: From 1 to the total number of servos. For each servos that you want to move you must specify those commands:
 *               
 *                3. Servo index: From 0 to the total number of servos minus 1. (Servos are meant to be connected in consecutive pins)
 *
 *      Example of input: 1 3 2 3 5 -> This command inquire if 3 have finished their movements: Servo no 2 , Servo no 3 and Servo no 5
 * DA MODIFICARE 
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
 * Example of input: 2 90 20 5 30 -> This command cause 2 stepper to move simultaneously: the Stepper no 0 to move the axis to 90% of maximum displacement moving the gear at 20 speed , then after reaching the displacemnt it start bouncing up and down of 5 millimiterss with gear speed of 30;
 *                                                                                                            in parallel it also cause the Stepper no 1 to move the axis to 10% of maximum displacement moving the gear at 30 speed , then after reaching the displacemnt it start bouncing up and down of 3 millimiterss with gear speed of 20
 */

#include <Arduino.h>
#include "servo_controller.h"
#include "stepper_controller.h"
#define MAX_COMMAND_LENGTH 500

unsigned long currentMillis;
int command[MAX_COMMAND_LENGTH];

void setup() {
  Serial.begin(9600);
  initializeServos();
  initializeStepper();
  while (Serial.available() <= 0) {
    Serial.println("ack");
    delay(100);
  }
}

void loop() {
  if (Serial.available() > 0) {
    int commandIndex = 0;

    while (Serial.available() > 0) {
      command[commandIndex] = Serial.parseInt();
      commandIndex++;
    }

    if (command[0] == 0) {
      int i = 1;
      int totServo = command[i++];
      resetServo();
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
        addMovementServo(servoIndex, path, totMovement);
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

    if (command[0] == 2) {
      int i = 1;
      int totServo = command[i++];

      if(totServo == 0){
        resetAllServos();
      }
      else{
        resetServo(command[i++], true);
        while(i< totServo){
          resetServo(command[i++], false);
        }
      }
    }

    if(command[0] == 3){
      addMovementStepper(command[1], command[2] , command[3], command[4]);
    }
  }
  
  currentMillis = millis();
  
  updateServos(currentMillis);
  updateStepper(currentMillis);
}