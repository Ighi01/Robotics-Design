#ifndef SERVO_CONTROLLER_H
#define SERVO_CONTROLLER_H
#define MAX_SERVO 20
#define MAX_MOVEMENTS 10
#define MAX_SPEED 100 //setted to 100 in order to make the cpu "rest" for 10 ms at every loop , more/equal than that we use the "instant" transmission
#define MIN_SPEED 5 //avoid division by 0
#include <Servo.h>
#include <Vector.h>

int NUM_SERVOS;

struct ServoData {
  Servo servo;
  int previousAngle;
  int angle; //must be integer
  unsigned long previousMillis;
  unsigned long previousDelayMillis;
  int numMovements;
  int movementIndex;
  int movements[MAX_MOVEMENTS]; //degree
  int delays[MAX_MOVEMENTS]; //sec
  int speeds[MAX_MOVEMENTS]; //degree/sec
};

ServoData servos[MAX_SERVO];

void initializeServos(int num_servos, int initialPin) {
  NUM_SERVOS = num_servos;
  for (int i = 0; i < NUM_SERVOS; i++) {
    servos[i].servo.attach(initialPin + i);
    servos[i].previousAngle = 0;
    servos[i].angle = 0;
    servos[i].previousMillis = 0;
    servos[i].previousDelayMillis = 0;
    servos[i].numMovements = 0;   
    servos[i].movementIndex = 0;
    memset(servos[i].movements, 0, sizeof(servos[i].movements));
    memset(servos[i].delays, 0, sizeof(servos[i].delays));
  }
}

void updateAngles(unsigned long currentMillis) {
  for (int i = 0; i < NUM_SERVOS; i++) {  
    if (servos[i].movementIndex < servos[i].numMovements) {
      if ((currentMillis - servos[i].previousDelayMillis)/1000 >= servos[i].delays[servos[i].movementIndex]) {

          servos[i].previousDelayMillis = currentMillis;
          servos[i].angle = servos[i].movements[servos[i].movementIndex];
          servos[i].movementIndex++;
      }
    }
  }
}

void updateServos(unsigned long currentMillis) {
  for (int i = 0; i < NUM_SERVOS; i++) {
    if (servos[i].previousAngle != servos[i].angle) {
      if(servos[i].speeds[servos[i].movementIndex >= MAX_SPEED){
        servos[i].servo.write(servos[i].angle);
      }
      else{
        int direction = (servos[i].angle > servos[i].previousAngle) ? 1 : -1 ;
        if (currentMillis - servos[i].previousMillis >= (1000/servos[i].speeds[servos[i].movementIndex])) {
          servos[i].previousMillis = currentMillis; 
          servos[i].servo.write(servos[i].previousAngle + direction);
          servos[i].previousAngle += direction;
        }
      }
    }
  }
}

void addMovement(int servoIndex, int num_movement, int movements_[], int delays_[], int speeds_[]) {
    servos[servoIndex].movementIndex = 0;
    servos[servoIndex].numMovements = num_movement;
    for (int i = 0; i < num_movement; i++) {
        servos[servoIndex].movements[i] = movements_[i];
        servos[servoIndex].delays[i] = delays_[i];
        if(speeds_[i] < MIN_SPEED){
          servos[servoIndex].speeds[i] = MIN_SPEED;
        }
        else{
          servos[servoIndex].speeds[i] = speeds_[i];
        }
    }
}

void printServoData() {
    for (int i = 0; i < NUM_SERVOS; i++) {
        Serial.print("Servo ");
        Serial.print(i);
        Serial.print(": ");
        Serial.print("Previous Angle: ");
        Serial.print(servos[i].previousAngle);
        Serial.print(", Current Angle: ");
        Serial.print(servos[i].angle);
        Serial.print(", Previous Delay: ");
        Serial.print(servos[i].previousDelay);
        Serial.print(", Num Movements: ");
        Serial.print(servos[i].numMovements);
        Serial.print(", Movement Index: ");
        Serial.println(servos[i].movementIndex);
        Serial.print("\n");
    }
}

#endif



