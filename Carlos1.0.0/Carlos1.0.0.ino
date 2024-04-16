#include <Stepper.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

const int stepsPerRevolution = 2048;
const int trig = 6;
const int echo = 5;
int duration = 0;
int distance = 0;
int counter1,counter2;
bool isUp = true;
unsigned long motorOffTime = 0, counterOff = 0;
LiquidCrystal_I2C lcd(0x27,16,2);
Stepper stepperName = Stepper(stepsPerRevolution, 8, 10, 9, 11);
Servo myServo;

void setup() {

  Serial.begin(9600); 
  pinMode(2,INPUT);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(12, OUTPUT);
  stepperName.setSpeed(16);
  stepperName.step(-stepsPerRevolution / 4);
  isUp = false;
  myServo.attach(13);
  lcd.init();
  lcd.backlight();
  counter1=0;
  counter2=0;
}

void loop() {

  int soundValue = analogRead(A0);
  int pirStat = digitalRead(3);
  //Serial.println(soundValue);

  if(soundValue > 150){
    int i=0;
    while(i<4){
      i++;
      myServo.write(30);
      delay(100); 
      myServo.write(-30);
      delay(100); 
    }    
  }

  if(pirStat == HIGH){
    myServo.write(180);
    stepperName.step(stepsPerRevolution / 6 );
  }

  digitalWrite(trig, HIGH);
  delayMicroseconds(1000);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration/58;
  //Serial.println(distance);

  if (distance <= 6) {
    if(millis() >= counterOff)
    {
      counter1++;
      digitalWrite(12, HIGH);
      motorOffTime = millis() + 1000;
      counterOff = millis() + 2000;
      if(isUp){
        stepperName.step(-stepsPerRevolution / 2);
        isUp = false;
      }
    }
  }

  if (distance >= 18 && distance <= 24) {
    if(millis() >= counterOff)
    {
      counter2++;
      digitalWrite(12, HIGH);
      motorOffTime = millis() + 1000;
      counterOff = millis() + 2000;
      if(!isUp)
      {
        stepperName.step(stepsPerRevolution / 2);
        isUp = true;
      }
    }
  }

  if (distance> 6 && distance <18 || distance >24) {
    stepperName.step(0);
  }

  if (millis() >= motorOffTime) {
    digitalWrite(12, LOW); 
  }

  lcd.setCursor(0,0);
  lcd.print("Sushi : ");
  lcd.print(counter1);
  lcd.setCursor(0,1);  
  lcd.print("Pizza : ");
  lcd.print(counter2);

}
