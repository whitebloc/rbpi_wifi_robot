#define NBCHAR 5
int rec;
char type[NBCHAR + 1];
int LED0 = 2; //car headlight
int LED1 = 3; //right turn signal
int LED2 = 4; //left turn signal
int LED3 = 5; //rear light
int LED4 = 6; //red light when car head light activated
int LED5 = 7; //brake lights
void setup() 
{
  Serial.begin(9600);
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
  delay(50);
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
  if (strcmp(type, "LED01") == 0)
  {
    //Serial.println("LED0 active");
    Serial.print("LED01");
    digitalWrite(LED0, HIGH);
  }
  else if (strcmp(type, "LED00") == 0)
  {
    //Serial.println("LED0 desactive");
    Serial.print("LED00");
    digitalWrite(LED0, LOW);
  }
  else if (strcmp(type, "LED11") == 0)
  {
    //Serial.println("LED1 active");
    Serial.println("LED11");
    digitalWrite(LED1, HIGH);
  }

  else if (strcmp(type, "LED10") == 0)
  {
    //Serial.println("LED1 desactive");
    Serial.println("LED10");
    digitalWrite(LED1, LOW);
  }

  else if (strcmp(type, "LED21") == 0)
  {
    //Serial.println("LED2 active");
    Serial.println("LED21");
    digitalWrite(LED2, HIGH);
  }

  else if (strcmp(type, "LED20") == 0)
  {
    //Serial.println("LED2 desactive");
    Serial.println("LED20");
    digitalWrite(LED2, LOW);
  }

  else if (strcmp(type, "LED31") == 0)
  {
    //Serial.println("LED3 active");
    Serial.println("LED31");
    digitalWrite(LED3, HIGH);
  }

  else if (strcmp(type, "LED30") == 0)
  {
    //Serial.println("LED3 desactive");
    Serial.println("LED30");
    digitalWrite(LED3, LOW);
  }

  else if (strcmp(type, "LED41") == 0)
  {
    //Serial.println("LED4 desactive");
    Serial.println("LED41");
    digitalWrite(LED4, HIGH);
  }

  else if (strcmp(type, "LED40") == 0)
  {
    //Serial.println("LED4 desactive");
    Serial.println("LED40");
    digitalWrite(LED4, LOW);
  }
  else if (strcmp(type, "LED51") == 0)
  {
    //Serial.println("LED5 desactive");
    Serial.println("LED51");
    digitalWrite(LED5, HIGH);
  }
  else if (strcmp(type, "LED50") == 0)
  {
    //Serial.println("LED5 desactive");
    Serial.println("LED50");
    digitalWrite(LED5, LOW);
  }


}
