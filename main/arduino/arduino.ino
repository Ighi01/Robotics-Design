/*

  This function serves as a serial command handler for controlling multiple servo motors and an stepper motor simultaneously controlling one side of the robot
  
  Serial command arguments **must** be separated by a **space** in the following order:

 * 1. Command number: 0, 1, 2 or 3.
 *
 *    - 0: Add new movements to the servo motors. If this is the command chosed, the following should be:  
 *           
 *               2. Number of Servo: From 1 to the total number of servos. For each servos that you want to move you must specify those commands:
 *  
 *               3. Servo index: From 0 to the total number of servos minus 1. In particular we have that:
 *
 *                    Servo 0 = Upper Mouth
 *                    Servo 1 = Lower Mouth
 *                    Servo 2 = Neck for Up and Down
 *                    Servo 3 = Neck for Left and Right
 *                    Servo 4 = Arm
 * 
 *               4. Number of movements to assign to the servo (0 to 15).
 * 
 *               5. For each movement assigned to the servo, must specify in order:
 *
 *                   - Angle to assign to the servo (in degrees, must be integer).
 *                   - Delay after the previous movement to start the movement (in seconds, must be integer). The 0 delays will make the movemnt start immediatelly after the previous is finished (or immediatelly if there is no one movement before)
 *                   - Movement speed in degrees per second (int degree/seconds, must be integer).
 *                   - Type of movement: from 0 to 4. In particular we have that:
 *
 *                          Type 0 = Linear 
 *                          Type 1 = Quadratic
 *                          Type 2 = Cube
 *                          Type 3 = Sine
 *                          Type 4 = Bounce
 * 
 *                  NOTE: The number of movements specified must match the number of quadruplets provided. All those arguments must be separated by space ,too
 * 
 *              NOTE: The number of servo specified must match the number of servos then provided. All those arguments must be separated by space ,too
 *
 *          Example of input: 0 2 0 2 90 0 90 0 0 5 100 1 3 1 60 0 30 4 -> This command 0 cause 2 servo to move simultaneously: the Servo no 0 to do 2 movements = move to 90 degrees immediatelly (0 delay) at 90 deg/sec velocity with type of movement linear and then after 5 seconds 
 *                                                                                                                                                                 from when the prevoius movement started move to 0 degrees at 100 deg/sec with type of movement Quadratic, then finish; 
 *                                                                                                                              In parallel the Servo no3 will also do 1 movement = move of 60 degrees immediatelly at 30 deg/sec velocity with type of movement Bounce, then finish.
 *
 *    - 1: Inquire whether the given servo motors have all finished their execution (return 1 if all the movements of all the given servos are completed, 0 if not). If this is the command chosed the following should be: 
 *
 *               2. Number of Servo: From 1 to the total number of servos : put 0 here if you want to inquire if all the servos have finished, otherwise for each servos that you want to inquire you must also specify those commands:
 *               
 *               3. Servo index: From 0 to the total number of servos minus 1. In particular we have that:
 *
 *                        Servo 0 = Upper Mouth
 *                        Servo 1 = Lower Mouth
 *                        Servo 2 = Neck for Up and Down
 *                        Servo 3 = Neck for Left and Right
 *                        Servo 4 = Arm
 *
 *          Example of input: 1 2 3 4 -> This will return 1 if both servo 3 and 4 have finished all of their movements , 0 otherwise.
 *
 *    - 2: Reset the given servo motors immediatelly to their initial position (even if it was moving into another angle). If this is the command chosed the following should be: 
 *
 *               2. Number of Servo: From 1 to the total number of servos : put 0 here if you want to reset all the servo, otherwise for each servos that you want to move you must also specify those commands:
 *               
 *               3. Servo index: From 0 to the total number of servos minus 1. In particular we have that:
 *
 *                        Servo 0 = Upper Mouth
 *                        Servo 1 = Lower Mouth
 *                        Servo 2 = Neck for Up and Down
 *                        Servo 3 = Neck for Left and Right
 *                        Servo 4 = Arm
 *
 *          Example of input: 2 0 -> This will make all the servos reset.
 *
 *    - 3: Add new movements to the stepper motor. If this is the command chosed, the following should be:  
 * 
 *               2. Percentage (must be integer) of displacent of the axis (0 if is at the origin, 100 is it is at maximum displacement wrt the origin)
 * 
 *               3. Velocity of the gear (must be integer) : maximum speed = 33
 * 
 *               4. Lenght of the debouncing that the axis start to do after reaching the wanted displacement (in millimeters, must be integer) : 0 for no bouncing, if this value is greather then the maximum value of debouncing = 0.5 centimeter it will saturate at this value
 * 
 *               5. Velocity of the gear for the bouncing (must be integer) : maximum speed = 33
 *
 *          Example of input: 3 90 20 5 30 -> This command 3 cause the Stepper to move the axis to 90% of maximum displacement moving the gear at 20 speed , then after reaching the displacemnt it start bouncing up and down of 5 millimiterss with gear speed of 30.
 *
 */

#include <Arduino.h>
#include "servo_controller.h"
#include "stepper_controller.h"
#define MAX_COMMAND_LENGTH 400
int command[MAX_COMMAND_LENGTH];
unsigned long currentMillis, previuousMillis;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(3000);
  initializeServos();
  initializeStepper();
  while (Serial.available() <= 0) {
    Serial.println("ack");
    delay(100);
  }
  Serial.end();
  Serial.begin(9600);
}

void loop() {

  //TODO : add control on the correctness of the input
  
  if (Serial.available() > 2) {

    int commandIndex = 0;
    int lenght = Serial.parseInt();

    while (commandIndex < lenght) {
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
        while (i < (4*totMovement + h)) {
          path[j].ang = command[i++];
          path[j].del = command[i++];
          path[j].speed = command[i++];
          path[j++].type = command[i++];
        }
        addMovementServo(servoIndex, path, totMovement);
      }
      Undone();
    }

    if (command[0] == 1) {
      int i = 1;
      int totServo = command[i++];

      if(totServo == 0){
        resetAllServos();
      }
      else{
        while(i< (totServo + 2)){
          resetServo(command[i++]);
        }
      }
      Undone();
    }

    if(command[0] == 2){
      addMovementStepper(command[1], command[2] , command[3], command[4]);
    }
  }
  currentMillis = millis();
  updateServos(currentMillis);
  updateStepper(currentMillis);
}