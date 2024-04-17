#include <Stepper.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

// SETTINGS /////////////////////////////////////////////////////////
const int MIC_THRESHOLD = 200;
const int INTERACTION_WINDOW = 30;
const String VALUE_1 = "Sushi";
const String VALUE_2 = "Pizza";


// COMPONENTS ///////////////////////////////////////////////////////

// sonar sensor
const int trig = 6;
const int echo = 5;

// Stepper Motor
const int stepsPerRevolution = 2048;
Stepper arm_stepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

// beep and fan
const int beep_and_fan = 12;

// microphone
const int mic = A0;

// LCD
LiquidCrystal_I2C lcd(0x27,16,2);

// Servo Motor
Servo mouth_servo;


// VARIABLES ////////////////////////////////////////////////////////
bool inInteraction = false;
int timePassed = 0;
int counter1, counter2 = 0;


// FUNCTIONS ////////////////////////////////////////////////////////
// microphone
int readMic() {
  return analogRead(A0);
}

// sonar sensor
void initSonar() {
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
}

int readDistance() {
  digitalWrite(trig, HIGH);
  delayMicroseconds(1000);
  digitalWrite(trig, LOW);
  return pulseIn(echo, HIGH)/58;
}

// arm
void initArm() {
  arm_stepper.setSpeed(16);
}
void moveArm(float turns) {
  arm_stepper.step(turns * stepsPerRevolution);
}
void wave() {
  moveArm(-0.1);
  moveArm(0.1);
  moveArm(-0.1);
  moveArm(0.1);
  moveArm(-0.1);
  moveArm(0.1);
}

// beep and fan
void initBeepAndFan() {
  pinMode(beep_and_fan, OUTPUT);
}
void beep() {
  digitalWrite(beep_and_fan, HIGH);
  delay(1000);
  digitalWrite(beep_and_fan, LOW);
}

// mouth
void initMouth() {
  mouth_servo.attach(13);
  mouth_servo.write(60);
}
void openMouth() {
  mouth_servo.write(-50);
}
void closeMouth() {
  mouth_servo.write(50);
}
void chew(int times) {
  for (int i = 0; i < times; i++) {
    openMouth();
    delay(300);
    closeMouth();
    delay(300);
  }
}

// LCD
void printLCD(int line, String text) {
  lcd.setCursor(0, line);
  lcd.print(text);
}
void initLCD() {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  printLCD(0, VALUE_1 + " : " + counter1);
  printLCD(1, VALUE_2 + " : " + counter2);
}


// votes
void vote1() {
  counter1 ++;
  printLCD(0, VALUE_1 + " : " + counter1);
}
void vote2() {
  counter2 ++;
  printLCD(1, VALUE_2 + " : " + counter2);
}


// SETUP ////////////////////////////////////////////////////////////
void setup() {
  Serial.begin(9600);
  initLCD();
  initMouth();
  initSonar();
  initBeepAndFan();
  initArm();

  beep();
}


// LOOP /////////////////////////////////////////////////////////////
void loop() {
  // interaction
  if (inInteraction && timePassed < INTERACTION_WINDOW) {
    int distance = readDistance();

    if (distance <= 22 && distance >= 3) {
      if (distance <= 9 && distance >= 3) {
        chew(4);
        vote1();
      }
      else if (distance >= 15 && distance <= 22) vote2();
      beep();

      // finish interaction
      timePassed = INTERACTION_WINDOW;
    }

    delay(1000);
    timePassed ++;
  }
  // end interaction
  else if (timePassed >= INTERACTION_WINDOW) {
    timePassed = 0;
    inInteraction = false;
    closeMouth();
    wave();
  }
  // start interaction
  else {
    int micValue = readMic();
    if (micValue > MIC_THRESHOLD) {
      inInteraction = true;
      wave();
      openMouth();
    }
  }


  // //Sound Sensor Input
  // int soundValue = analogRead(A0);

  // //Sound Sensor Routine
  // if(soundValue > 150){
  //   int i=0;
  //   while(i<1){
  //     i++;
  //     mouth_servo.write(40);
  //   }    
  // }

  // //Sonar Sensor Input
  // digitalWrite(trig, HIGH);
  // delayMicroseconds(1000);
  // digitalWrite(trig, LOW);
  // duration = pulseIn(echo, HIGH);
  // distance = duration/58;

  // //Sonar Sensor Routine
  // if (distance <= 6) {
  //   if(millis() >= counterOff)
  //   {
  //     counter1++;

  //     //LCD prints
  //     lcd.setCursor(0,0);
  //     lcd.print("Sushi : ");
  //     lcd.print(counter1);

  //     digitalWrite(beep_and_fan, HIGH);

  //     motorOffTime = millis() + 1000;
  //     counterOff = millis() + 2000;

  //     if(isUp){
  //       arm_stepper.step(-stepsPerRevolution / 2);
  //       isUp = false;
  //     }

  //     i=0;
  //     while(i<3){
  //       i++;
  //       mouth_servo.write(-45);
  //       delay(1000);
  //       mouth_servo.write(45);
  //       delay(1000);
  //     }

  //   }
  // }

  // if (distance >= 13.5 && distance <= 19) {
  //   if(millis() >= counterOff)
  //   {
  //     counter2++;

  //     //LCD prints
  //     lcd.setCursor(0,1);  
  //     lcd.print("Pizza : ");
  //     lcd.print(counter2);

  //     digitalWrite(beep_and_fan, HIGH);

  //     motorOffTime = millis() + 1000;
  //     counterOff = millis() + 2000;

  //     if(!isUp)
  //     {
  //       arm_stepper.step(stepsPerRevolution / 2);
  //       isUp = true;
  //     }
      
  //     i=0;
  //     while(i<3){
  //       i++;
  //       mouth_servo.write(-45);
  //       delay(1000);
  //       mouth_servo.write(45);
  //       delay(1000);
  //     }
      
  //   }
  // }

  // if (millis() >= motorOffTime) {
  //   digitalWrite(12, LOW); 
  // }
}
