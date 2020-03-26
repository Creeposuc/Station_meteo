
#include "DHT.h"
#define DHTPIN 8
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
float lum = 0;  // variable to store the value read
float temp = 0;
void setup() {
  Serial.begin(9600);           //  setup serial
  dht.begin();
}

void loop() {
  lum = analogRead(A0);
  temp = analogRead(A1);// read the input pin
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
   if (isnan(h) || isnan(t)) {
    float h = 0;
    float t = 0;
    return;
  }
  
  Serial.println(">>>");
  //Serial.println("luminosité");
  Serial.println(h); 
  //Serial.println("température");
  Serial.println(t);
  //temp = (temp*0.0481);
  //delay(2400000);
  delay(2000);
}
