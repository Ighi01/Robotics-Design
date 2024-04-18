#ifndef SERVO_CONTROLLER_H
#define SERVO_CONTROLLER_H
#define MAX_SERVO 20
#define MAX_MOVEMENTS 10
#define MAX_SPEED 100 //setted to 100 in order to make the cpu "rest" for 10 ms at every loop , more/equal than that we use the "instant" transmission
#define MIN_SPEED 5 //avoid division by 0
#include <Servo.h>

int NUM_SERVOS;
int INITIAL_PIN;
int servoType;

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
    int delay;
    int speed;
};

ServoData servos[MAX_SERVO];

void addMovement(int servoIndex, Movement path[]) {
    servos[servoIndex].movementIndex = 0;
    servos[servoIndex].numMovements = sizeof(path[0]);
    for (int i = 0; i < servos[servoIndex].numMovements; i++) {
        if (servoType == 1) {
            servos[servoIndex].angles[i] = path[i].ang + 90;
            if (servos[servoIndex].angles[i] == 0) {
                servos[servoIndex].angles[i] = 1;
            }
        }
        else {
            servos[servoIndex].angles[i] = path[i].ang;
        }
        servos[servoIndex].delays[i] = path[i].delay;
        if (path[i].speed < MIN_SPEED) {
            servos[servoIndex].speeds[i] = MIN_SPEED;
        }
        else {
            servos[servoIndex].speeds[i] = path[i].speed;
        }
    }
    servos[servoIndex].angle = servos[servoIndex].angles[0];
}

void initializeServos(int num_servos, int initialPin, int type) {
    NUM_SERVOS = num_servos;
    INITIAL_PIN = initialPin;
    servoType = type;
    for (int i = 0; i < NUM_SERVOS; i++) {
        servos[i].servo.attach(INITIAL_PIN + i); //servos should be one after the other
        servos[i].previousMillis = 0;
        servos[i].previousDelayMillis = 0;
        servos[i].numMovements = 0;
        servos[i].movementIndex = 0;
        memset(servos[i].angles, 0, sizeof(servos[i].angles));
        memset(servos[i].delays, 0, sizeof(servos[i].delays));
        if (servoType == 1) {
            servos[i].servo.write(91);
            servos[i].previousAngle = 91;
            servos[i].angle = 91;
        }
        else {
            servos[i].servo.write(1);
            servos[i].previousAngle = 1;
            servos[i].angle = 1;
        }
    }
}

void updateServos(unsigned long currentMillis) {
    //Move servos
    for (int i = 0; i < NUM_SERVOS; i++) {
        if (servos[i].previousAngle != servos[i].angle) {
            if (servos[i].speeds[servos[i].movementIndex] >= MAX_SPEED) {
                servos[i].servo.write(servos[i].angle);
                servos[i].previousAngle = servos[i].angle;
            }
            else {
                int direction = (servos[i].angle > servos[i].previousAngle) ? 1 : -1;
                if (currentMillis - servos[i].previousMillis >= (1000 / servos[i].speeds[servos[i].movementIndex])) {
                    servos[i].previousMillis = currentMillis;
                    servos[i].servo.write(servos[i].previousAngle + direction);
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

bool isComplete(int servoIndex) {
    return servos[servoIndex].movementIndex == (servos[servoIndex].numMovements - 1) && servos[servoIndex].previousAngle == servos[servoIndex].angle;
}

void printServoData() {
    for (int i = 0; i < NUM_SERVOS; i++) {
        Serial.print("Servo ");
        Serial.print(i);
        Serial.print(": ");
        Serial.print(", Current Angle: ");
        Serial.print(servos[i].angle);
        Serial.print(", Is Complete: ");
        Serial.println(isComplete(i));
        Serial.print("\n");
    }
}

#endif