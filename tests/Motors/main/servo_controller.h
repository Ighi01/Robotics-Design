#ifndef SERVO_CONTROLLER_H
#define SERVO_CONTROLLER_H

//Hyperparameters
#define NUM_SERVOS 10
#define INITIAL_PIN 2
#define MAX_MOVEMENTS 20
#define MAX_SPEED 100 //setted to 100 in order to make the cpu "rest" for 10 ms at every loop , more/equal than that we use the "instant" transmission
#define MIN_SPEED 5 //avoid division by 0
#define MIN_MICRO 300 // SG90 around 0 degree 
//

#include <Servo.h>

//THIS LIBRARY IS INTENDED TO WORK WITH SG90 

struct ServoData {
  Servo servo;
  int previousAngle;
  int angle; //must be integer
  unsigned long previousMillis;
  unsigned long previousDelayMillis;
  int numMovements;
  int movementIndex;
  int angles[MAX_MOVEMENTS]; //degree
  int delays[MAX_MOVEMENTS]; //sec
  int speeds[MAX_MOVEMENTS]; //degree/sec
};

struct Movement {
  int ang;
  int del;
  int speed;
};

ServoData servos[NUM_SERVOS];

void initializeServos() {
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].servo.attach(INITIAL_PIN + i); //servos should be one after the other
    servos[i].previousMillis = 0;
    servos[i].previousDelayMillis = 0;
    servos[i].numMovements = 0;
    servos[i].movementIndex = 0;
    memset(servos[i].angles, 0, sizeof(servos[i].angles));
    memset(servos[i].delays, 0, sizeof(servos[i].delays));
    servos[i].servo.writeMicroseconds(MIN_MICRO);
    servos[i].previousAngle = 0;
    servos[i].angle = 0;
  }
}

void addMovementServo(int servoIndex, Movement path[], int numEl ,unsigned long currentMillis) {
  servos[servoIndex].movementIndex = 0;
  servos[servoIndex].numMovements = numEl;
  servos[servoIndex].previousMillis = currentMillis;                  
  servos[servoIndex].previousDelayMillis = currentMillis;
  for (int i = 0; i < servos[servoIndex].numMovements; i++) {
    servos[servoIndex].angles[i] = path[i].ang;
    servos[servoIndex].delays[i] = path[i].del;
    if (path[i].speed < MIN_SPEED) {
      servos[servoIndex].speeds[i] = MIN_SPEED;
    }
    else {
      servos[servoIndex].speeds[i] = path[i].speed;
    }
  }
  servos[servoIndex].angle = servos[servoIndex].angles[0];
}

void updateServos(unsigned long currentMillis) {
  //Move servos
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (servos[i].previousAngle != servos[i].angle) {
      if (servos[i].speeds[servos[i].movementIndex] >= MAX_SPEED) {
        servos[i].servo.writeMicroseconds((servos[i].angle*10)+MIN_MICRO);
        servos[i].previousAngle = servos[i].angle;
      }
      else {
        int direction = (servos[i].angle > servos[i].previousAngle) ? 1 : -1;
        if (currentMillis - servos[i].previousMillis >= (1000 / servos[i].speeds[servos[i].movementIndex])) {
          servos[i].previousMillis = currentMillis;
          servos[i].servo.writeMicroseconds(((servos[i].previousAngle + direction)*10)+MIN_MICRO);
          servos[i].previousAngle += direction;
        }
      }
    }
  }
  //Update Angles
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (servos[i].movementIndex < servos[i].numMovements - 1) {
      if ((currentMillis - servos[i].previousDelayMillis) / 1000 >= servos[i].delays[servos[i].movementIndex + 1]) {
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