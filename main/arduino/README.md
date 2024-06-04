# Arduino Code for Robotics Design
This repository contains the Arduino code for the Robotics and Design Group 4 project.

## Structure

The key files are:

- `arduino.ino`: The main Arduino sketch file. This file includes the setup and loop functions, which are the entry points for the Arduino program.
- `servo_controller.h`: This header file contains the definitions and functions for controlling the servo motors.
- `stepper_controller.h`: This header file contains the definitions and functions for controlling the stepper motor.

## Usage

To use this code, upload the arduino.ino sketch to your Arduino board using the Arduino IDE.

The setup() function initializes the servos and stepper motor. The loop() function reads commands from the serial port and performs the corresponding actions on the motors.

This function serves as a serial command handler for controlling multiple servo motors and an stepper motor simultaneously controlling one side of the robot
  
Serial command arguments **must** be separated by a **space** in the following order:

0. Total numbers in the command (do not consider spaces)

1. Command number: 0, 1, or 2.

   - 0: Add new movements to the servo motors. If this is the command chosed, the following should be:  
          
              2. Number of Servo: From 1 to the total number of servos. For each servos that you want to move you must specify those commands:
 
              3. Servo index: From 0 to the total number of servos minus 1. In particular we have that:

                   Servo 0 = Upper Mouth
                   Servo 1 = Lower Mouth
                   Servo 2 = Neck for Up and Down
                   Servo 3 = Neck for Left and Right
                   Servo 4 = Arm

              4. Number of movements to assign to the servo (0 to 15).

              5. For each movement assigned to the servo, must specify in order:

                  - Angle to assign to the servo (in degrees, must be integer).
                  - Delay after the previous movement to start the movement (in seconds, must be integer). The 0 delays will make the movemnt start immediatelly after the previous is finished (or immediatelly if there is no one movement before)
                  - Movement speed in degrees per second (int degree/seconds, must be integer).
                  - Type of movement: from 0 to 4. In particular we have that:

                         Type 0 = Linear 
                         Type 1 = Quadratic
                         Type 2 = Cube
                         Type 3 = Sine
                         Type 4 = Bounce

                 NOTE: The number of movements specified must match the number of quadruplets provided. All those arguments must be separated by space ,too

             NOTE: The number of servo specified must match the number of servos then provided. All those arguments must be separated by space ,too

         Example of input: 18 0 2 0 2 90 0 90 0 0 5 100 1 3 1 60 0 30 4 -> This command 0 cause 2 servo to move simultaneously: the Servo no 0 to do 2 movements = move to 90 degrees immediatelly (0 delay) at 90 deg/sec velocity with type of movement linear and then after 5 seconds 
                                                                                                                                                                from when the prevoius movement started move to 0 degrees at 100 deg/sec with type of movement Quadratic, then finish; 
                                                                                                                                In parallel the Servo no3 will also do 1 movement = move of 60 degrees immediatelly at 30 deg/sec velocity with type of movement Bounce, then finish.

   - 1: Reset the given servo motors immediatelly to their initial position (even if it was moving into another angle). If this is the command chosed the following should be: 

              2. Number of Servo: From 1 to the total number of servos : put 0 here if you want to reset all the servo, otherwise for each servos that you want to move you must also specify those commands:
              
              3. Servo index: From 0 to the total number of servos minus 1. In particular we have that:

                       Servo 0 = Upper Mouth
                       Servo 1 = Lower Mouth
                       Servo 2 = Neck for Up and Down
                       Servo 3 = Neck for Left and Right
                       Servo 4 = Arm

         Example of input: 2 2 0 -> This will make all the servos reset.

   - 3: Add new movements to the stepper motor. If this is the command chosed, the following should be:  

              2. Percentage (must be integer) of displacent of the axis (0 if is at the origin, 100 is it is at maximum displacement wrt the origin)

              3. Velocity of the gear (must be integer) : maximum speed = 33

              4. Lenght of the debouncing that the axis start to do after reaching the wanted displacement (in millimeters, must be integer) : 0 for no bouncing, if this value is greather then the maximum value of debouncing = 0.5 centimeter it will saturate at this value

              5. Velocity of the gear for the bouncing (must be integer) : maximum speed = 33

         Example of input: 5 3 90 20 5 30 -> This command 3 cause the Stepper to move the axis to 90% of maximum displacement moving the gear at 20 speed , then after reaching the displacemnt it start bouncing up and down of 5 millimiterss with gear speed of 30.

## Dependencies

This code depends on the Arduino standard library, and the Stepper.h, Servo.h and ServoEasing librares for controlling stepper motors and servos. All dependencies are included in the `lib` directory.
