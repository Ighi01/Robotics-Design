#ifndef STEPPER_CONTROLLER_H
#define STEPPER_CONTROLLER_H
#include <Stepper.h>

#define STEPS_PER_REVOLUTION 1024
#define MAX_SPEED 36
#define MIN_SPEED 15

#define LENGTH 11.4           //lenght of the bar in centimeters
#define RADIOUS_GEAR 0.0025   //radious of the gear in meters                 NOTE: those two values have been tuned wrt real values due to some imperpections 
#define MAX_DEBOUNCING 0.5    //lenght of the maximum bouncing in centimeters
#define FLOATING_TIME 1000    //milliseconds (should be greater then 10 ms)

int fullTurn = 0.01 * ((LENGTH - MAX_DEBOUNCING) / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION;
int maxDebTurn = 0.01 * (MAX_DEBOUNCING / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION;
Stepper stepper = Stepper(STEPS_PER_REVOLUTION, 2, 7, 4, 8);

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

StepperData stepperData;

void move(){
  if(stepperData.actual < stepperData.goal){
    stepper.step(stepperData.direction);
    stepperData.actual ++;
  }
}

void setSpeed(int speed){  
  if (speed < MIN_SPEED) {
    speed = MIN_SPEED;
  } else if (speed > MAX_SPEED) {
    speed = MAX_SPEED;
  }  
  stepper.setSpeed(speed);  
}

void addStep(int step){
  int direction = 1;
  if(step < 0)
  {
    step *= -1;
    direction *= -1;
  }  
  stepperData.actual = 0;
  stepperData.goal = step;
  stepperData.direction = direction;
}

void initializeStepper() {
  stepperData.percentage = 0;
  stepperData.bounceStep = 0;
  stepperData.timeToFloat = 0;
  stepperData.bounceVelocity = 0;
  stepperData.previousMillis = 0;
  stepperData.goUp = false;

  setSpeed(MAX_SPEED);  
  addStep(-fullTurn);

  while(stepperData.actual < stepperData.goal) {
    move();
  }
  
  addStep(maxDebTurn);

  while(stepperData.actual < stepperData.goal) {
    move();
  }
}

void addMovementStepper(int percentage, int velocity, int bounceStep, int bounceVelocity, unsigned long currentMillis) {

  int step;

  if (stepperData.goUp) {   
    step = fullTurn * 0.01 * (percentage - stepperData.percentage) + stepperData.bounceStep - (stepperData.actual - stepperData.goal) * stepperData.direction;
  }
  else{
    step = fullTurn * 0.01 * (percentage - stepperData.percentage) - (stepperData.actual - stepperData.goal) * stepperData.direction;
  }

  setSpeed(velocity);
  addStep(step);

  stepperData.percentage = percentage;
  stepperData.previousMillis = currentMillis;
  stepperData.bounceStep = bounceStep >= (MAX_DEBOUNCING * 10) ? maxDebTurn : maxDebTurn * (bounceStep / (10 * MAX_DEBOUNCING));
  stepperData.bounceVelocity = bounceVelocity;
  stepperData.goUp = false;
}

void updateStepper(unsigned long currentMillis) {  
  if (stepperData.actual < stepperData.goal){
    move();
  }
  else if (stepperData.bounceStep > 0 && (currentMillis - stepperData.previousMillis) > FLOATING_TIME) {
    
    setSpeed(stepperData.bounceVelocity);

    if (stepperData.goUp) {
      addStep(stepperData.bounceStep);
      stepperData.goUp = false;
    } else {
      addStep(-stepperData.bounceStep);
      stepperData.goUp = true;
    }
    stepperData.previousMillis = currentMillis;
  }
}

#endif
