#ifndef SERVO_CONTROLLER_H
#define SERVO_CONTROLLER_H

//Hyperparameters
<<<<<<< Updated upstream
#define NUM_SERVOS 5
#define MAX_MOVEMENTS 10

#define PROVIDE_ONLY_LINEAR_MOVEMENT 
#include <ServoEasing.hpp> 
=======
#define NUM_SERVOS 12
#define INITIAL_PIN 2
#define MAX_MOVEMENTS 7 
#define MAX_SPEED 100 //setted to 100 in order to make the cpu "rest" for 10 ms at every loop , more/equal than that we use the "instant" transmission
#define MIN_SPEED 5 //avoid division by 0

#include <ServoEasing.hpp>
#define PROVIDE_ONLY_LINEAR_MOVEMENT

//THIS LIBRARY IS INTENDED TO WORK WITH SG90 
>>>>>>> Stashed changes

struct ServoData {
  ServoEasing servo;
  int previousAngle;
  int angle; //must be integer
  unsigned long previousMillis;
  unsigned long previousDelayMillis;
  int numMovements;
  int movementIndex;
  int angles[MAX_MOVEMENTS]; //degree
  int delays[MAX_MOVEMENTS]; //sec
  int speeds[MAX_MOVEMENTS]; //degree/sec

  int initialAngle;
  int resetSpeed;
};

struct Movement {
  int ang;
  int del;
  int speed;
};

ServoData servos[NUM_SERVOS];

void initializeServos() {

  servos[0].initialAngle = 0; 
  servos[1].initialAngle = 0;
  servos[2].initialAngle = 0;
  servos[3].initialAngle = 0; 
  servos[4].initialAngle = 2; //ARM
  
  servos[0].resetSpeed = 1000; 
  servos[1].resetSpeed = 1000;
  servos[2].resetSpeed = 1000;
  servos[3].resetSpeed = 1000; 
  servos[4].resetSpeed = 25; //ARM

  servos[0].servo.attach(3,servos[0].initialAngle); 
  servos[1].servo.attach(5,servos[1].initialAngle);
  servos[2].servo.attach(6,servos[2].initialAngle);
  servos[3].servo.attach(9,servos[3].initialAngle); 
  servos[4].servo.attach(10,servos[4].initialAngle); //ARM

  for (int i = 0; i < NUM_SERVOS; i++) {
<<<<<<< Updated upstream
=======
    servos[i].servo.attach(INITIAL_PIN + i,0); //servos should be one after the other
>>>>>>> Stashed changes
    servos[i].previousMillis = 0;
    servos[i].previousDelayMillis = 0;
    servos[i].numMovements = 0;
    servos[i].movementIndex = 0;
    memset(servos[i].angles, 0, sizeof(servos[i].angles));
    memset(servos[i].delays, 0, sizeof(servos[i].delays));
<<<<<<< Updated upstream
    servos[i].previousAngle = servos[i].initialAngle;
    servos[i].angle = servos[i].initialAngle;
=======
    //servos[i].servo.write(0);
    servos[i].previousAngle = 0;
    servos[i].angle = 0;
>>>>>>> Stashed changes
  }
}

void addMovementServo(int servoIndex, Movement path[], int numEl) {
  servos[servoIndex].movementIndex = 0;
  servos[servoIndex].numMovements = numEl;
  
  for (int i = 0; i < servos[servoIndex].numMovements; i++) {
    servos[servoIndex].angles[i] = path[i].ang;
    servos[servoIndex].delays[i] = path[i].del;
    servos[servoIndex].speeds[i] = path[i].speed;
  }
  servos[servoIndex].angle = servos[servoIndex].angles[0];

  stopAllServos();

  //Reset Servo before starting new movement
  for (int i = 0; i < NUM_SERVOS; i++) {
    bool firstOne = true;
    if(firstOne){
      servos[i].servo.startEaseTo(servos[i].initialAngle, servos[i].resetSpeed);
      firstOne = false;
    }
    else{
      servos[i].servo.setEaseTo(servos[i].initialAngle, servos[i].resetSpeed);
    }
    servos[i].previousAngle = servos[i].initialAngle;
  }
  
  //Wait until are servo are resetted
  while (ServoEasing::areInterruptsActive()) {
    delay(10);
  }

 
  servos[servoIndex].previousMillis = millis();                  
  servos[servoIndex].previousDelayMillis = millis();
}

void updateServos(unsigned long currentMillis) {
  //Move servos
  for (int i = 0; i < NUM_SERVOS; i++) {
<<<<<<< Updated upstream
    bool firstOne = true;
=======
    /*
>>>>>>> Stashed changes
    if (servos[i].previousAngle != servos[i].angle) {
      if(firstOne){
        servos[i].servo.startEaseTo(servos[i].angle, servos[i].speeds[servos[i].movementIndex]);
        firstOne = false;
      }
      else{
        servos[i].servo.setEaseTo(servos[i].angle, servos[i].speeds[servos[i].movementIndex]);
      }
      servos[i].previousAngle = servos[i].angle;
    }
     */
    if (servos[i].previousAngle != servos[i].angle) {
      servos[i].servo.setEasingType(EASE_CUBIC_IN_OUT);
      servos[i].servo.startEaseTo(servos[i].angle, servos[i].speeds[servos[i].movementIndex]);
      servos[i].previousAngle = servos[i].angle;
    }
  
  }
  //Update Angles
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (servos[i].movementIndex < servos[i].numMovements - 1) {
      if ((currentMillis - servos[i].previousDelayMillis) / 1000 >= servos[i].delays[servos[i].movementIndex + 1]) {
        if(!servos[i].servo.isMoving())
        servos[i].movementIndex++;
        servos[i].previousDelayMillis = currentMillis;
        servos[i].angle = servos[i].angles[servos[i].movementIndex];
      }
    }
  }
}

bool isCompleteServo(int servoIndex) {
  return (servos[servoIndex].movementIndex == (servos[servoIndex].numMovements - 1) || servos[servoIndex].numMovements == 0) && servos[servoIndex].previousAngle == servos[servoIndex].angle;
}

#endif