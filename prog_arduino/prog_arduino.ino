int i = 0;
#include "SR04.h"
#define TRIG_PIN 4
#define ECHO_PIN 3
SR04 sr04 = SR04(ECHO_PIN,TRIG_PIN);
long a;
float angle;
#include <Stepper.h>
const int stepsPerRevolution = 800;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);
void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(20);
}

void loop() {
  a=sr04.Distance();
  Serial.print(a + "\n");
  if (Serial.available()) {
    angle = Serial.read();
    myStepper.step(angle);
  }
}
