
float lum = 0;  // variable to store the value read
float temp = 0;
void setup() {
  Serial.begin(9600);           //  setup serial
}

void loop() {
  lum = analogRead(A0);
  temp = analogRead(A1);// read the input pin
  Serial.println(">>>");
  //Serial.println("luminosité");
  Serial.println(lum); 
  //Serial.println("température");
  Serial.println(temp);
  //temp = (temp*0.0481);
  //delay(2400000);
  delay(1000);
}
