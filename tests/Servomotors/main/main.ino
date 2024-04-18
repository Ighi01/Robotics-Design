#include <Arduino.h>
#include "servo_controller.h"

  // Servos must be in consecutive pins starting from INITIAL_PIN_SERVOS pin
  // Each movement in the path is composed by 3 field : angle (degres), delay (sec) wrt last movement from which the movement take place, speed (degres/sec)
  // Angles must be from -90 to 90 (not 0) for g90 (type 0) , 1 to 180 for others (type 1) and must be integer values : path should be made take in consideration -90 to 90 reference, then algorith adjust it automatically based on the type of the servo
  // Speeds over 100 degree/sec are fed into immediate transactions
  // First movement delay must be 0 
  // addMovement requires the pin of the interested servo, the number of movement we want to add , followed by the path 
  // Every time we add a movement with addMovement we overwrite the previous path added 

//SERVO
const int SERVOS = 4;
const int INITIAL_PIN_SERVOS = 2;
const int mouthPin = 2 - INITIAL_PIN_SERVOS;
const int armPin1 = 3 - INITIAL_PIN_SERVOS;
const int armPin2 = 4 - INITIAL_PIN_SERVOS;
const int armPin3 = 5 - INITIAL_PIN_SERVOS;
const int typeServo = 1; //0 for g90 , 1 for others

//IR
const int irPin = 8;
const long irInterval = 100;
unsigned long previousMillisIR = 0;
bool irValue, irOldValue;

//PRINT
static unsigned long previousMillisPrint = 0;

unsigned long currentMillis;

Movement loopPath[3][6] = {
  { {1,0,90} , {50,5,90} , {-90,4,90} , {10,2,90}, {-30,6,90} , {1,10,90} },
  { {1,0,90} , {-40,5,90} , {90,4,60} , {10,2,80}, {-60,6,30} , {1,10,90} },
  { {1,0,90} , {20,5,75} , {-40,4,90} , {-60,2,80}, {30,6,45} , {1,10,90} }
};

void setup() {

  Serial.begin(9600);
  initializeServos(SERVOS,INITIAL_PIN_SERVOS,typeServo);
  pinMode(irPin, INPUT);

  addMovement(mouthPin, 6, loopPath[0] , typeServo); 
  addMovement(armPin1, 6, loopPath[1], typeServo);
  addMovement(armPin2, 6, loopPath[2], typeServo);
}

void loop() {

  if(isComplete(mouthPin)) addMovement(mouthPin, 6, loopPath[0], typeServo);
  if(isComplete(armPin1)) addMovement(armPin1, 6, loopPath[1], typeServo);
  if(isComplete(armPin2)) addMovement(armPin2, 6, loopPath[2], typeServo);
 
  currentMillis = millis();

  if (currentMillis - previousMillisIR >= irInterval) {
    previousMillisIR = currentMillis;
    irValue = digitalRead(irPin);
    
    if (!irValue && irOldValue) {    
      Movement path_3[6] = { {1,0,90} , {-20,5,60} , {40,4,90} , {60,2,80}, {-30,6,45} , {1,10,90} }; 
      addMovement(armPin2, 6, path_3, typeServo);
      
      Movement path[4] = { {1,0,90} , {40,7.5,60} , {-70,10,90} , {1,5,90} }; 
      addMovement(armPin3, 4, path, typeServo);
    }

    irOldValue = irValue;
  }

  if (currentMillis - previousMillisPrint >= 5000) {
    previousMillisPrint = currentMillis;
    
    Serial.println(currentMillis/1000);
    printServoData();
    
  }

  updateServos(currentMillis);
  delay(10);

}