#ifndef STEPPER_CONTROLLER_H
#define STEPPER_CONTROLLER_H

//Hyperparameters
#define NUM_STEPPER 2
#define INITIAL_PIN 2
#define STEPS_PER_REVOLUTION 100
#define LENGTH 40 //centimeters
#define MAX_DEBOUNCING 3 //centimeters
#define RADIOUS_GEAR 0.01 //meters
#define FLOATING_TIME 1000 //milliseconds (should be greater then 10 ms)
//

#include <Stepper.h>

struct StepperData {
  Stepper stepper;
  int percentage; //integer
  int bounceStep; //in meters
  int timeToFloat;
  int bounceVelocity; //rpm
  bool goUp;
  unsigned long previousMillis;

  StepperData() : stepper(STEPS_PER_REVOLUTION, 0, 0, 0, 0) {}

  void setPins(int motor_pin_1, int motor_pin_2, int motor_pin_3, int motor_pin_4) {
    stepper = Stepper(STEPS_PER_REVOLUTION, motor_pin_1, motor_pin_2, motor_pin_3, motor_pin_4);
  }

  void setSpeed(int rpm) {
    stepper.setSpeed(rpm);
  }

  void step(int steps) {
    stepper.step(steps);
  }
};

StepperData steppers[NUM_STEPPER];

void initializeSteppers() {
  for (int i = 0; i < NUM_STEPPER; i++) {
    steppers[i].setPins(INITIAL_PIN + 4*i, INITIAL_PIN + 1 + 4*i, INITIAL_PIN + 2 + 4*i, INITIAL_PIN + 3 + 4*i);
    steppers[i].percentage = 0;
    steppers[i].bounceStep = 0;
    steppers[i].timeToFloat = 0;
    steppers[i].bounceVelocity = 0;
    steppers[i].previousMillis = 0;
    steppers[i].goUp = true;
  }
}

void addMovementStepper(int stepperIndex, int percentage, int velocity, int bounceStep, int bounceVelocity, unsigned long currentMillis) {
  double step = 0.01 * ((LENGTH - MAX_DEBOUNCING) / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION * 0.01 * (percentage - steppers[stepperIndex].percentage);
  if (!steppers[stepperIndex].goUp) {
    step -= steppers[stepperIndex].bounceStep;
  }

  steppers[stepperIndex].setSpeed(velocity);
  steppers[stepperIndex].step(step);

  steppers[stepperIndex].percentage = percentage;
  steppers[stepperIndex].previousMillis = currentMillis;
  steppers[stepperIndex].bounceStep = bounceStep > MAX_DEBOUNCING ? (0.01 * (MAX_DEBOUNCING / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION) : (0.01 * (bounceStep / (6.28 * RADIOUS_GEAR)) * STEPS_PER_REVOLUTION);
  steppers[stepperIndex].timeToFloat = fmod(1000 * (60.0 / velocity) * (step / STEPS_PER_REVOLUTION), 1.0);
  steppers[stepperIndex].bounceVelocity = bounceVelocity;
  steppers[stepperIndex].goUp = true;
}

void updateSteppers(unsigned long currentMillis) {
  for (int i = 0; i < NUM_STEPPER; i++) {
    if (steppers[i].bounceStep > 0 && (currentMillis - steppers[i].previousMillis) > steppers[i].timeToFloat) {

      steppers[i].setSpeed(steppers[i].bounceVelocity);

      if (steppers[i].goUp) {
        steppers[i].step(steppers[i].bounceStep);
        steppers[i].goUp = false;
      } else {
        steppers[i].step(-steppers[i].bounceStep);
        steppers[i].goUp = true;
      }
      steppers[i].previousMillis = currentMillis;
      steppers[i].timeToFloat = FLOATING_TIME;
    }
  }
}

#endif
