#ifndef SERVO_CONTROLLER_H
#define SERVO_CONTROLLER_H

//Hyperparameters
#define NUM_SERVOS 5
#define MAX_MOVEMENTS 10

#define PROVIDE_ONLY_LINEAR_MOVEMENT 
#include <ServoEasing.hpp> 

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

  servos[0].initialAngle = 5; //MOUTH DOWN
  servos[1].initialAngle = 5; //MOUTH UP
  servos[2].initialAngle = 25; //NECK LXR
  servos[3].initialAngle = 45; //NECK UXD
  servos[4].initialAngle = 2; //ARM
  
  servos[0].resetSpeed = 100; //MOUTH DOWN
  servos[1].resetSpeed = 100; //MOUTH UP
  servos[2].resetSpeed = 25; //NECK LXR
  servos[3].resetSpeed = 25; //NECK UXD
  servos[4].resetSpeed = 25; //ARM

  servos[0].servo.attach(3,servos[0].initialAngle); 
  servos[1].servo.attach(5,servos[1].initialAngle);
  servos[2].servo.attach(6,servos[2].initialAngle);
  servos[3].servo.attach(9,servos[3].initialAngle); 
  servos[4].servo.attach(10,servos[4].initialAngle); //ARM

  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].previousMillis = 0;
    servos[i].previousDelayMillis = 0;
    servos[i].numMovements = 0;
    servos[i].movementIndex = 0;
    memset(servos[i].angles, 0, sizeof(servos[i].angles));
    memset(servos[i].delays, 0, sizeof(servos[i].delays));
    servos[i].previousAngle = servos[i].initialAngle;
    servos[i].angle = servos[i].initialAngle;
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
}

void resetServo(){

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
    servos[i].angle = servos[i].initialAngle;
  }
  
  //Wait until are servo are resetted
  while (ServoEasing::areInterruptsActive()) {
    delay(10);
  }
}

void updateServos(unsigned long currentMillis) {
  //Move servos
  for (int i = 0; i < NUM_SERVOS; i++) {
    bool firstOne = true;
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