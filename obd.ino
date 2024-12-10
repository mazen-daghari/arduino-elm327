#include <SoftwareSerial.h>
#include <ELMduino.h>

SoftwareSerial mySerial(10, 11); // RX, TX
ELM327 myELM327;

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);

  if (!myELM327.begin(mySerial)) {
    Serial.println("Couldn't connect to OBD-II adapter. Please check connections and try again.");
    while (1);
  }
}

void loop() {
  float rpm = myELM327.rpm();
  float speed = myELM327.kph();
  float coolantTemp = myELM327.engineCoolantTemp();
  float fuelLevel = myELM327.fuelLevel();

  if (rpm > 0 && speed > 0 && coolantTemp > 0 && fuelLevel >= 0) {
    Serial.print(rpm); Serial.print(",");
    Serial.print(speed); Serial.print(",");
    Serial.print(coolantTemp); Serial.print(",");
    Serial.print(fuelLevel); Serial.println(",");
  } else {
    Serial.println("ELM327 error: Could not read one or more values.");
  }

  delay(1000); // Wait for 1 second before the next loop
}
