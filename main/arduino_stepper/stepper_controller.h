#ifndef STEPPER_CONTROLLER_H
#define STEPPER_CONTROLLER_H

//Hyperparameters
#define NUM_STEPPER 2
#define INITIAL_PIN 2
#define STEPS_PER_REVOLUTION 1024
#define LENGTH 12.5 //centimeters (little bit less)
#define MAX_DEBOUNCING 1 //centimeters
#define RADIOUS_GEAR 0.0025 //meters
#define FLOATING_TIME 1000 //milliseconds (should be greater then 10 ms)

#include <Stepper.h>
#include <EEPROM.h>
Stepper stepper1 = Stepper(STEPS_PER_REVOLUTION, INITIAL_PIN, INITIAL_PIN+2, INITIAL_PIN+1, INITIAL_PIN+3);
Stepper stepper2 = Stepper(STEPS_PER_REVOLUTION, INITIAL_PIN+4, INITIAL_PIN+6, INITIAL_PIN+5, INITIAL_PIN+7);

struct StepperData {
  int percentage; //integer
  int bounceStep; //in meters
  int timeToFloat;
  int bounceVelocity; //rpm
  bool goUp;
  unsigned long previousMillis;
};

StepperData steppers[NUM_STEPPER];

void speed(int speed, int stepperIndex){
  if (stepperIndex == 0){    
    stepper1.setSpeed(speed);
  }

  if (stepperIndex == 1){    
    stepper2.setSpeed(speed);
  }
}

void step_(int step, int stepperIndex){
  if (stepperIndex == 0){        
    stepper1.step(-step);
  }

  if (stepperIndex == 1){        
    stepper2.step(-step);
  }
}

void initializeSteppers() {
  for (int i = 0; i < NUM_STEPPER; i++) {
    steppers[i].percentage = 0;
    steppers[i].bounceStep = 0;
    steppers[i].timeToFloat = 0;
    steppers[i].bounceVelocity = 0;
    steppers[i].previousMillis = 0;
    steppers[i].goUp = true;
    
    //double step = 0.01 * ((LENGTH - MAX_DEBOUNCING) / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION * 0.08; 
    //EEPROM.write(i, (MAX_DEBOUNCING/LENGTH)*100);
    double step = 0.01 * ((LENGTH - MAX_DEBOUNCING) / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION * 0.01 * ((MAX_DEBOUNCING/LENGTH)*100 - EEPROM.read(i)); 
    speed(30, i);
    step_(step, i);
  }
}

void addMovementStepper(int stepperIndex, int percentage, int velocity, int bounceStep, int bounceVelocity, unsigned long currentMillis) {
  double step = 0.01 * ((LENGTH - MAX_DEBOUNCING) / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION * 0.01 * (percentage - steppers[stepperIndex].percentage);
  if (!steppers[stepperIndex].goUp) {
    step -= steppers[stepperIndex].bounceStep;
  }

  speed(velocity,stepperIndex);
  step_(step,stepperIndex);

  steppers[stepperIndex].percentage = percentage;
  EEPROM.write(stepperIndex, percentage);
  steppers[stepperIndex].previousMillis = currentMillis;
  steppers[stepperIndex].bounceStep = bounceStep > MAX_DEBOUNCING ? (0.01 * (MAX_DEBOUNCING / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION) : (0.01 * (bounceStep / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION);
  steppers[stepperIndex].timeToFloat = fmod(1000 * (60.0 / velocity) * (step / STEPS_PER_REVOLUTION), 1.0);
  steppers[stepperIndex].bounceVelocity = bounceVelocity;
  steppers[stepperIndex].goUp = true;
}

void updateSteppers(unsigned long currentMillis) {
  for (int i = 0; i < NUM_STEPPER; i++) {
    if (steppers[i].bounceStep > 0 && (currentMillis - steppers[i].previousMillis) > steppers[i].timeToFloat) {
      
      speed(steppers[i].bounceVelocity,i);

      if (steppers[i].goUp) {
        step_(steppers[i].bounceStep,i);
        steppers[i].goUp = false;
      } else {
        
        step_(-steppers[i].bounceStep,i);
        steppers[i].goUp = true;
      }
      steppers[i].previousMillis = currentMillis;
      steppers[i].timeToFloat = FLOATING_TIME;
    }
  }
}

#endif
