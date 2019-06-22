
int a = 0;
void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.print(a + "\n");
  if (Serial.available()) {
    Serial.read();
  }
}
