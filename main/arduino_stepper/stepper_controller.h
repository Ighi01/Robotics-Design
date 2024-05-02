#ifndef STEPPER_CONTROLLER_H
#define STEPPER_CONTROLLER_H
#include <Stepper.h>

//Hyperparameters
#define NUM_STEPPER 2
#define INITIAL_PIN 2

#define STEPS_PER_REVOLUTION 1024
#define DIRECTION -1
#define MAX_SPEED 30
#define MIN_SPEED 15

#define LENGTH 11.4           //lenght of the bar in centimeters
#define RADIOUS_GEAR 0.0025   //radious of the gear in meters                 NOTE: those two values have been tuned wrt real values due to some imperpections 
#define MAX_DEBOUNCING 0.5    //lenght of the maximum bouncing in centimeters
#define FLOATING_TIME 1000    //milliseconds (should be greater then 10 ms)

int fullTurn = 0.01 * ((LENGTH - MAX_DEBOUNCING) / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION;
int maxDebTurn = 0.01 * (MAX_DEBOUNCING / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION;
Stepper stepper1 = Stepper(STEPS_PER_REVOLUTION, INITIAL_PIN, INITIAL_PIN+2, INITIAL_PIN+1, INITIAL_PIN+3);
Stepper stepper2 = Stepper(STEPS_PER_REVOLUTION, INITIAL_PIN+4, INITIAL_PIN+6, INITIAL_PIN+5, INITIAL_PIN+7);

struct StepperData {
  int percentage; //integer
  int bounceStep; 
  int timeToFloat;
  int bounceVelocity;
  bool goUp;
  unsigned long previousMillis;
};

StepperData steppers[NUM_STEPPER];

void speed(int speed, int stepperIndex){
  
  if (speed < MIN_SPEED) {
    speed = MIN_SPEED;
  } else if (speed > MAX_SPEED) {
    speed = MAX_SPEED;
  }

  if (stepperIndex == 0){    
    stepper1.setSpeed(speed);
  }

  if (stepperIndex == 1){    
    stepper2.setSpeed(speed);
  }
}

void step_(int step, int stepperIndex){
  if (stepperIndex == 0){        
    stepper1.step(step * DIRECTION);
  }

  if (stepperIndex == 1){        
    stepper2.step(step * DIRECTION);
  }
}

void initializeSteppers() {
  for (int i = 0; i < NUM_STEPPER; i++) {
    steppers[i].percentage = 0;
    steppers[i].bounceStep = 0;
    steppers[i].timeToFloat = 0;
    steppers[i].bounceVelocity = 0;
    steppers[i].previousMillis = 0;
    steppers[i].goUp = false;

    speed(MAX_SPEED, i);  
    step_(-fullTurn, i);
    step_(maxDebTurn, i);
  }
}

void addMovementStepper(int stepperIndex, int percentage, int velocity, int bounceStep, int bounceVelocity, unsigned long currentMillis) {

  while(steppers[stepperIndex].bounceStep > 0 && steppers[stepperIndex].goUp && (currentMillis - steppers[stepperIndex].previousMillis) < steppers[stepperIndex].timeToFloat) {
    currentMillis = millis();
  }

  int step = fullTurn * 0.01 * (percentage - steppers[stepperIndex].percentage);
  
  if (steppers[stepperIndex].goUp) {   
    speed(steppers[stepperIndex].bounceVelocity,stepperIndex);     
    step_(steppers[stepperIndex].bounceStep,stepperIndex);
    steppers[stepperIndex].goUp = false;
  }

  speed(velocity,stepperIndex);
  step_(step,stepperIndex);

  steppers[stepperIndex].percentage = percentage;
  steppers[stepperIndex].previousMillis = currentMillis;
  steppers[stepperIndex].bounceStep = bounceStep >= (MAX_DEBOUNCING * 10) ? maxDebTurn : maxDebTurn * (bounceStep / (10 * MAX_DEBOUNCING));
  steppers[stepperIndex].timeToFloat = fmod(1000 * (60.0 / velocity) * (step / STEPS_PER_REVOLUTION), 1.0);
  steppers[stepperIndex].bounceVelocity = bounceVelocity;
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
