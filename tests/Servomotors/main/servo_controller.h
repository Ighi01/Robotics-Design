#ifndef SERVO_CONTROLLER_H
#define SERVO_CONTROLLER_H
#define MAX_SERVO 20
#define MAX_MOVEMENTS 10

#include <Servo.h>
#include <Vector.h>

int NUM_SERVOS;
unsigned long INTERVAL;
unsigned long increment; //NOTE: angle % increment == 0 !

struct ServoData {
  Servo servo;
  int previousAngle;
  int angle;
  unsigned long previousMillis;
  int previousDelay;
  int numMovements;
  int movementIndex;
  int movements[MAX_MOVEMENTS];
  int delays[MAX_MOVEMENTS];
};

ServoData servos[MAX_SERVO];

void initializeServos(int num_servos, int initialPin, unsigned long interval, unsigned long increment_) {
  NUM_SERVOS = num_servos;
  INTERVAL = interval;
  increment = increment_;
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].servo.attach(initialPin + i);
    servos[i].previousAngle = 0;
    servos[i].angle = 0;
    servos[i].previousMillis = 0;
    servos[i].previousDelay = 0;
    servos[i].numMovements = 0;   
    servos[i].movementIndex = 0;
    memset(servos[i].movements, 0, sizeof(servos[i].movements));
    memset(servos[i].delays, 0, sizeof(servos[i].delays));
  }
}

void updateAngle(int servoIndex, unsigned long currentMillis) {
    if (servos[servoIndex].movementIndex < servos[servoIndex].numMovements) {
        if (currentMillis - servos[servoIndex].previousDelay >= servos[servoIndex].delays[servos[servoIndex].movementIndex] * 1000) {

            servos[servoIndex].previousDelay = currentMillis;
            servos[servoIndex].angle = servos[servoIndex].movements[servos[servoIndex].movementIndex];
            servos[servoIndex].movementIndex++;
        }
    }
}

void updateServos(unsigned long currentMillis) {
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (servos[i].previousAngle != servos[i].angle) {
      int direction = (servos[i].angle > servos[i].previousAngle) ? 1 : -1 ;
         
      if (currentMillis - servos[i].previousMillis >= INTERVAL) {
        servos[i].previousMillis = currentMillis; 
        servos[i].servo.write(servos[i].previousAngle + direction*increment);
        servos[i].previousAngle += direction;
      }
    }
    else{
      updateAngle(i,currentMillis);
    }
  }
}

void addMovement(int servoIndex, const int num_movement,const int movements_[], const int delays_[]) {
    servos[servoIndex].movementIndex = 0;
    servos[servoIndex].numMovements = num_movement;
    for (int i = 0; i < num_movement; i++) {
        servos[servoIndex].movements[i] = movements_[i];
        servos[servoIndex].delays[i] = delays_[i];
    }
}

#endif



