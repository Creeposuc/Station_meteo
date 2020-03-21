int valeur = "0";

void setup() {
  // Opens serial port, sets data rate to 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // Sends a line over serial:
  //Serial.println("test");
  //Serial.println("--------------");
  int valeur = "0";
  if (Serial.available() > 0){
    valeur = Serial.read();
    char message = valeur;
    Serial.println(message);
  }
  delay(20000);
  if (valeur == "1"){
    Serial.println("valeur");
  }
}
