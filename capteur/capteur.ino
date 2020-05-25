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
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
   if (isnan(h) || isnan(t)) {
    float h = 0;
    float t = 0;
    return;
  }
  
  Serial.println(">>>");
  Serial.println(h); 
  Serial.println(t);
  delay(900);
}
