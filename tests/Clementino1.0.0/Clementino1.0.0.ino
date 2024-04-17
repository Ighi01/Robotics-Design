#include <Stepper.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

const int stepsPerRevolution = 2048;
const int trig = 6;
const int echo = 5;
const int buzz_dc_motor = 12;
const int mic = A0;
int duration = 0;
int distance = 0;
int counter1 = 0,counter2 = 0,i;
bool isUp = false;
unsigned long motorOffTime = 0, counterOff = 0;
LiquidCrystal_I2C lcd(0x27,16,2);
Stepper stepperName = Stepper(stepsPerRevolution, 8, 10, 9, 11);
Servo myServo;

void setup() {

  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(buzz_dc_motor, OUTPUT);

  stepperName.setSpeed(16);
  stepperName.step(-stepsPerRevolution / 4);

  myServo.attach(13);

  lcd.init();
  lcd.backlight();
}

void loop() {

  //Sound Sensor Input
  int soundValue = analogRead(A0);

  //Sound Sensor Routine
  if(soundValue > 150){
    int i=0;
    while(i<1){
      i++;
      myServo.write(40);
    }    
  }

  //Sonar Sensor Input
  digitalWrite(trig, HIGH);
  delayMicroseconds(1000);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration/58;

  //Sonar Sensor Routine
  if (distance <= 6) {
    if(millis() >= counterOff)
    {
      counter1++;

      //LCD prints
      lcd.setCursor(0,0);
      lcd.print("Sushi : ");
      lcd.print(counter1);

      digitalWrite(buzz_dc_motor, HIGH);

      motorOffTime = millis() + 1000;
      counterOff = millis() + 2000;

      if(isUp){
        stepperName.step(-stepsPerRevolution / 2);
        isUp = false;
      }

      i=0;
      while(i<3){
        i++;
        myServo.write(-45);
        delay(1000);
        myServo.write(45);
        delay(1000);
      }

    }
  }

  if (distance >= 13.5 && distance <= 19) {
    if(millis() >= counterOff)
    {
      counter2++;

      //LCD prints
      lcd.setCursor(0,1);  
      lcd.print("Pizza : ");
      lcd.print(counter2);

      digitalWrite(buzz_dc_motor, HIGH);

      motorOffTime = millis() + 1000;
      counterOff = millis() + 2000;

      if(!isUp)
      {
        stepperName.step(stepsPerRevolution / 2);
        isUp = true;
      }
      
      i=0;
      while(i<3){
        i++;
        myServo.write(-45);
        delay(1000);
        myServo.write(45);
        delay(1000);
      }
      
    }
  }

  if (millis() >= motorOffTime) {
    digitalWrite(12, LOW); 
  }

}
