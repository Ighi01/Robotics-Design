#ifndef STEPPER_CONTROLLER_H
#define STEPPER_CONTROLLER_H
#include <Stepper.h>

#define NUM_STEPPER 2
#define INITIAL_PIN 2

#define STEPS_PER_REVOLUTION 1024
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

  int actual;
  int goal;
  int direction;
};

StepperData steppers[NUM_STEPPER];

void move(int stepperIndex){
  if(steppers[stepperIndex].actual < steppers[stepperIndex].goal){
    if (stepperIndex == 0){  
      stepper1.step(steppers[stepperIndex].direction);
    }
    if (stepperIndex == 1){
      stepper2.step(steppers[stepperIndex].direction);
    }
    steppers[stepperIndex].actual ++;
  }
}

void setSpeed(int speed, int stepperIndex){  
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

void addStep(int step, int stepperIndex){
  int direction = 1;
  if(step < 0)
  {
    step *= -1;
    direction *= -1;
  }  
  steppers[stepperIndex].actual = 0;
  steppers[stepperIndex].goal = step;
  steppers[stepperIndex].direction = direction;
}

void initializeSteppers() {
  for (int i = 0; i < NUM_STEPPER; i++) {
    steppers[i].percentage = 0;
    steppers[i].bounceStep = 0;
    steppers[i].timeToFloat = 0;
    steppers[i].bounceVelocity = 0;
    steppers[i].previousMillis = 0;
    steppers[i].goUp = false;

    setSpeed(MAX_SPEED, i);  
    addStep(-fullTurn, i);
  }

  while(steppers[0].actual < steppers[0].goal && steppers[1].actual < steppers[1].goal) {
    if(steppers[0].actual < steppers[0].goal) move(0);
    if(steppers[1].actual < steppers[1].goal) move(1);
  }

  for (int i = 0; i < NUM_STEPPER; i++) {  
    addStep(maxDebTurn, i);
  }

  while(steppers[0].actual < steppers[0].goal && steppers[1].actual < steppers[1].goal) {
    if(steppers[0].actual < steppers[0].goal) move(0);
    if(steppers[1].actual < steppers[1].goal) move(1);
  }
}

void addMovementStepper(int stepperIndex, int percentage, int velocity, int bounceStep, int bounceVelocity, unsigned long currentMillis) {

  int step;

  if (steppers[stepperIndex].goUp) {   
    step = fullTurn * 0.01 * (percentage - steppers[stepperIndex].percentage) + steppers[stepperIndex].bounceStep - (steppers[stepperIndex].actual - steppers[stepperIndex].goal) * steppers[stepperIndex].direction;
  }
  else{
    step = fullTurn * 0.01 * (percentage - steppers[stepperIndex].percentage) - (steppers[stepperIndex].actual - steppers[stepperIndex].goal) * steppers[stepperIndex].direction;
  }

  setSpeed(velocity,stepperIndex);
  addStep(step,stepperIndex);

  steppers[stepperIndex].percentage = percentage;
  steppers[stepperIndex].previousMillis = currentMillis;
  steppers[stepperIndex].bounceStep = bounceStep >= (MAX_DEBOUNCING * 10) ? maxDebTurn : maxDebTurn * (bounceStep / (10 * MAX_DEBOUNCING));
  steppers[stepperIndex].bounceVelocity = bounceVelocity;
  steppers[stepperIndex].goUp = false;
}

void updateSteppers(unsigned long currentMillis) {  
  for (int i = 0; i < NUM_STEPPER; i++) {
    if (steppers[i].actual < steppers[i].goal){
      move(i);
    }
    else if (steppers[i].bounceStep > 0 && (currentMillis - steppers[i].previousMillis) > FLOATING_TIME) {
      
      setSpeed(steppers[i].bounceVelocity,i);

      if (steppers[i].goUp) {
        addStep(steppers[i].bounceStep,i);
        steppers[i].goUp = false;
      } else {
        addStep(-steppers[i].bounceStep,i);
        steppers[i].goUp = true;
      }
      steppers[i].previousMillis = currentMillis;
    }
  }
}

#endif
