#ifndef SERVO_CONTROLLER_H
#define SERVO_CONTROLLER_H

#define NUM_SERVOS 5
#define MAX_MOVEMENTS 15

// TODO: do better code pins initialization

#define ENABLE_EASE_LINEAR
#define ENABLE_EASE_QUADRATIC
#define ENABLE_EASE_CUBIC
#define ENABLE_EASE_BOUNCE
#define ENABLE_EASE_SINE

#include <ServoEasing.hpp> 

struct ServoData {
  ServoEasing servo;
  int previousAngle;
  int angle; 
  unsigned long previousDelayMillis;
  int numMovements;
  int movementIndex;
  int angles[MAX_MOVEMENTS]; 
  int delays[MAX_MOVEMENTS]; 
  int speeds[MAX_MOVEMENTS]; 
  int types[MAX_MOVEMENTS];  
  int initialAngle;
  int resetSpeed;
  bool isReset;
};

struct Movement {
  int ang;
  int del;
  int speed;
  int type;
};

ServoData servos[NUM_SERVOS];

void rootServo(int servoIndex){
  servos[servoIndex].previousDelayMillis = 0;
  servos[servoIndex].numMovements = 0;
  servos[servoIndex].movementIndex = 0;
  memset(servos[servoIndex].angles, 0, sizeof(servos[servoIndex].angles));
  memset(servos[servoIndex].delays, 0, sizeof(servos[servoIndex].delays));
  memset(servos[servoIndex].delays, 0, sizeof(servos[servoIndex].speeds));
  memset(servos[servoIndex].delays, 0, sizeof(servos[servoIndex].types));
  servos[servoIndex].previousAngle = servos[servoIndex].initialAngle;
  servos[servoIndex].angle = servos[servoIndex].initialAngle;
}

void initializeServos() {

  servos[0].initialAngle = 40; // 40 ORANGE , 0 GREEN 
  servos[1].initialAngle = 40; // 40 ORANGE , 0 GREEN
  servos[2].initialAngle = 35; // 35 ORANGE , 50 GREEN
  servos[3].initialAngle = 30; // 30 ORANGE , 150 GREEN
  servos[4].initialAngle = 80; // 80 ORANGE , 0 GREEN

  servos[0].resetSpeed = 100;
  servos[1].resetSpeed = 100;
  servos[2].resetSpeed = 25; 
  servos[3].resetSpeed = 25; 
  servos[4].resetSpeed = 25;   
  
  //TODO: define limits of servo using myServo.setMinMaxConstraint(minMicroseconds, maxMicroseconds);
  //TODO: do it also for speeds
  
  servos[0].servo.attach(3,servos[0].initialAngle); //MOUTH DOWN
  servos[1].servo.attach(5,servos[1].initialAngle); //MOUTH UP
  servos[2].servo.attach(6,servos[2].initialAngle); //NECK UXD
  servos[3].servo.attach(9,servos[3].initialAngle); //NECK LXR
  servos[4].servo.attach(10,servos[4].initialAngle); //ARM

  for (int i = 0; i < NUM_SERVOS; i++) {
    rootServo(i);
    servos[i].isReset = false;
  }
}

void addMovementServo(int servoIndex, Movement path[], int numEl) {
  servos[servoIndex].movementIndex = 0;
  servos[servoIndex].numMovements = numEl;
  for (int i = 0; i < servos[servoIndex].numMovements; i++) {
    servos[servoIndex].angles[i] = path[i].ang;
    servos[servoIndex].delays[i] = path[i].del;
    servos[servoIndex].speeds[i] = path[i].speed;
    servos[servoIndex].types[i] = path[i].type;
  }
  servos[servoIndex].angle = servos[servoIndex].angles[0];
  servos[servoIndex].previousDelayMillis = millis();
}

void resetServo(int servoIndex){
  servos[servoIndex].servo.stop();
  servos[servoIndex].servo.setEasingType(EASE_LINEAR);
  servos[servoIndex].servo.startEaseTo(servos[servoIndex].initialAngle, servos[servoIndex].resetSpeed);
  rootServo(servoIndex);
  servos[servoIndex].isReset = true;
}

void resetAllServos(){
  for (int i = 0; i < NUM_SERVOS ; i++) {
    resetServo(i);
  }
}

void updateServos(unsigned long currentMillis) {
  // Move Servo    
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (servos[i].previousAngle != servos[i].angle && !servos[i].servo.isMoving()) {
      if(!servos[i].isReset){
        switch(servos[i].types[servos[i].movementIndex]){
          case 0:
            servos[i].servo.setEasingType(EASE_LINEAR);
            break;
          case 1:
            servos[i].servo.setEasingType(EASE_QUADRATIC_IN_OUT);
            break;
          case 2:
            servos[i].servo.setEasingType(EASE_CUBIC_IN_OUT);
            break;
          case 3:
            servos[i].servo.setEasingType(EASE_SINE_IN_OUT);
            break;
          case 4:
            servos[i].servo.setEasingType(EASE_BOUNCE_OUT);
            break;
          default:
            servos[i].servo.setEasingType(EASE_LINEAR);
            break;
        }
        servos[i].servo.startEaseTo(servos[i].angle, servos[i].speeds[servos[i].movementIndex]);
        servos[i].previousAngle = servos[i].angle;
      }
      else{
        if(!servos[i].servo.isMoving()){
          servos[i].isReset = false;
        }
      }
    }
  }
  //Update Angles
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (servos[i].movementIndex < servos[i].numMovements - 1) {
      if ((currentMillis - servos[i].previousDelayMillis) / 1000 >= servos[i].delays[servos[i].movementIndex + 1]) {
        if(!servos[i].servo.isMoving()){
          servos[i].movementIndex++;
          servos[i].previousDelayMillis = currentMillis;
          servos[i].angle = servos[i].angles[servos[i].movementIndex];
        }
      }
    }
  }
}

bool isAllCompleteServo(int servoIndex) {
  return (servos[servoIndex].movementIndex == (servos[servoIndex].numMovements - 1) || servos[servoIndex].numMovements == 0) && servos[servoIndex].previousAngle == servos[servoIndex].angle;
}

int isAllCompleteServos(){
  int result = 1;
  for (int i = 0; i < NUM_SERVOS; i++) {
    if(!isAllCompleteServo(i)){
      result = 0;
      break;
    }
  }
  return result;
}

#endif