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
const int SERVOS = 2;
const int INITIAL_PIN_SERVOS = 6;
const int mouthPin = 6;
const int armPin1 = 7;
const int armPin2 = 8;
const int armPin3 = 9;
const int typeServo = 0; //0 for g90 , 1 for others

//IR
const int irPin = 8;
const long irInterval = 100;
unsigned long previousMillisIR = 0;
bool irValue, irOldValue;

//PRINT
static unsigned long previousMillisPrint = 0;

unsigned long currentMillis;

void setup() {

  Serial.begin(9600);
  initializeServos(SERVOS,INITIAL_PIN_SERVOS);
  pinMode(irPin, INPUT);
  
  Movement path_1[6] = { {1,0,90} , {50,25,90} , {-90,10,90} , {10,15,90}, {-30,40,90} , {1,25,90} }; 
  addMovement(mouthPin, 6, path_1, typeServo); 
  
  Movement path_2[6] = { {1,0,90} , {-40,15,90} , {90,10,60} , {10,5,80}, {-60,20,30} , {1,25,90} }; 
  addMovement(armPin1, 6, path_2, typeServo);
  
  Movement path_3[6] = { {1,0,90} , {-20,15,60} , {40,10,90} , {60,5,80}, {-30,20,45} , {1,25,90} }; 
  addMovement(armPin2, 6, path_3, typeServo);
  
  Movement path_4[6] = { {1,0,90} , {20,15,75} , {-40,10,90} , {-60,5,80}, {30,20,45} , {1,25,90} }; 
  addMovement(armPin3, 6, path_4, typeServo);

}

void loop() {

  currentMillis = millis();

  if (currentMillis - previousMillisIR >= irInterval) {
    previousMillisIR = currentMillis;
    irValue = digitalRead(irPin);
    
    if (!irValue && irOldValue) {
      //setDelayedPosition(0, 45, 5000);
      //setDelayedPosition(1, 90, 5000);
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


