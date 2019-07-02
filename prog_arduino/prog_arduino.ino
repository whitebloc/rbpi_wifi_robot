#define NBCHAR 5
int rec;
char type[NBCHAR + 1];
int LED0 = 2; //car headlight
int LED1 = 3; //right turn signal
int LED2 = 4; //left turn signal
int LED3 = 5; //rear light
int LED4 = 6; //red light when car head light activated
int LED5 = 7; //brake lights
void setup() {
  Serial.begin(38400);
  pinMode(LED0, OUTPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
}

void loop() {
  comunication_decode_1();
  comunication_decode_2();
  delay (10);
}
void comunication_decode_1()
{
  for ( int i = 0; i < NBCHAR; )
  {
    if (Serial.available()) {
      rec = Serial.read();
    }
    if ( rec != -1 ) {
      type[i] = rec;
      i++;
      type[i] = "\0";
    }
  }
  return type;
}
void comunication_decode_2()
{
  if (strncmp(type, "BRAKE", NBCHAR) == 0)
  {
    //Serial.println("LED0 active");
    Serial.println("BRAKE");
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
    digitalWrite(LED3, LOW);
    digitalWrite(LED5, HIGH);
  }
  else if (strncmp(type, "FORWA", NBCHAR) == 0)
  {
    //Serial.println("LED0 desactive");
    Serial.println("FORWA");
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
    digitalWrite(LED3, LOW);
    digitalWrite(LED5, LOW);
  }
  else if (strncmp(type, "BACKW", NBCHAR) == 0)
  {
    //Serial.println("LED0 desactive");
    Serial.println("BACKW");
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
    digitalWrite(LED3, HIGH);
    digitalWrite(LED5, LOW);
  }
  else if (strncmp(type, "LEFT*", NBCHAR) == 0)
  {
    //Serial.println("LED1 active");
    Serial.println("LEFT*");
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, HIGH);
    digitalWrite(LED3, LOW);
    digitalWrite(LED5, LOW);
  }
  else if (strncmp(type, "RIGHT", NBCHAR) == 0)
  {
    //Serial.println("LED1 desactive");
    Serial.println("RIGHT");
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, LOW);
    digitalWrite(LED3, LOW);
    digitalWrite(LED5, LOW);
  }
  else if (strncmp(type, "LIGHT", NBCHAR) == 0)
  {
    //Serial.println("LED2 active");
    Serial.println("LIGHT");
    digitalWrite(LED0, HIGH);
    digitalWrite(LED4, HIGH);
  }
  else if (strncmp(type, "DARK*", NBCHAR) == 0)
  {
    //Serial.println("LED2 desactive");
    Serial.println("DARK*");
    digitalWrite(LED0, LOW);
    digitalWrite(LED4, LOW);
  }
}
