#include "HX711_ADC.h"

// Pins
const int HX711_dout_1 = 4; //mcu > HX711 no 1 dout pin
const int HX711_sck_1 = 5;  //mcu > HX711 no 1 sck pin

const int HX711_dout_2 = 6; //mcu > HX711 no 2 dout pin
const int HX711_sck_2 = 7;  //mcu > HX711 no 2 sck pin

const int HX711_dout_3 = 8; //mcu > HX711 no 3 dout pin
const int HX711_sck_3 = 9;  //mcu > HX711 no 3 sck pin

const int HX711_dout_4 = 10; //mcu > HX711 no 4 dout pin
const int HX711_sck_4 = 11;  //mcu > HX711 no 4 sck pin

const int HX711_dout_5 = 12; //mcu > HX711 no 5 dout pin
const int HX711_sck_5 = 13;  //mcu > HX711 no 5 sck pin

// HX711 constructor (dout pin, sck pin)
HX711_ADC LoadCell_b1(HX711_dout_1, HX711_sck_1); //HX711 1
HX711_ADC LoadCell_b2(HX711_dout_2, HX711_sck_2); //HX711 2
HX711_ADC LoadCell_g(HX711_dout_3, HX711_sck_3); //HX711 3
HX711_ADC LoadCell_b3(HX711_dout_4, HX711_sck_4); //HX711 4
HX711_ADC LoadCell_b4(HX711_dout_5, HX711_sck_5); //HX711 5

long t;

void setup() {
  Serial.begin(57600);
  delay(10);
  Serial.println();
  Serial.println("Starting...");

  float calibrationValue_b1 = -420.00; // calibration value load cell 1          !!!
  float calibrationValue_b2 = -418.53; // calibration value load cell 2
  float calibrationValue_g = -951.84;  // calibration value load cell 3
  float calibrationValue_b3 = -420.80; // calibration value load cell 4
  float calibrationValue_b4 = -416.38; // calibration value load cell 5

  LoadCell_b1.begin();
  LoadCell_b2.begin();
  LoadCell_b3.begin();
  LoadCell_b4.begin();
  LoadCell_g.begin();
  
  long stabilizingtime = 3000;  // tare preciscion can be improved by adding a few seconds of stabilizing time
  boolean _tare = true;         // set this to false if you don't want tare to be performed in the next step
  byte LoadCell_b1_rdy = 0;
  byte LoadCell_b2_rdy = 0;
  byte LoadCell_b3_rdy = 0;
  byte LoadCell_b4_rdy = 0;
  byte LoadCell_g_rdy = 0;
  while ((LoadCell_b1_rdy + LoadCell_b2_rdy + LoadCell_b3_rdy + LoadCell_b4_rdy+ LoadCell_g_rdy ) < 5) { // run startup, stabilization and tare, all modules simultaneously
    if (!LoadCell_b1_rdy)
      LoadCell_b1_rdy = LoadCell_b1.startMultiple(stabilizingtime, _tare);
    if (!LoadCell_b2_rdy)
      LoadCell_b2_rdy = LoadCell_b2.startMultiple(stabilizingtime, _tare);
    if (!LoadCell_b3_rdy)
      LoadCell_b3_rdy = LoadCell_b3.startMultiple(stabilizingtime, _tare);
    if (!LoadCell_b4_rdy)
      LoadCell_b4_rdy = LoadCell_b4.startMultiple(stabilizingtime, _tare);
    if (!LoadCell_g_rdy)
      LoadCell_g_rdy = LoadCell_g.startMultiple(stabilizingtime, _tare);
  }
  
  #if defined(DEBUG)
    if (LoadCell_b1.getTareTimeoutFlag()) {
      Serial.println("Timeout, check MCU>HX711 no.1 wiring and pin designations");
    }
    if (LoadCell_b2.getTareTimeoutFlag()) {
      Serial.println("Timeout, check MCU>HX711 no.2 wiring and pin designations");
    }
    if (LoadCell_b3.getTareTimeoutFlag()) {
      Serial.println("Timeout, check MCU>HX711 no.4 wiring and pin designations");
    }
    if (LoadCell_b4.getTareTimeoutFlag()) {
      Serial.println("Timeout, check MCU>HX711 no.5 wiring and pin designations");
    }
    if (LoadCell_g.getTareTimeoutFlag()) {
      Serial.println("Timeout, check MCU>HX711 no.3 wiring and pin designations");
    }
  #endif
  
  LoadCell_b1.setCalFactor(calibrationValue_b1); // user set calibration value (float)
  LoadCell_b2.setCalFactor(calibrationValue_b2); // user set calibration value (float)
  LoadCell_b3.setCalFactor(calibrationValue_b3); // user set calibration value (float)
  LoadCell_b4.setCalFactor(calibrationValue_b4); // user set calibration value (float)
  LoadCell_g.setCalFactor(calibrationValue_g);   // user set calibration value (float)
}

void loop() {
  static int initialized = 0;
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; // increase value to slow down serial print activity

  // Check for new data/start next conversion
  if (LoadCell_b1.update())
    newDataReady = true;
  if (LoadCell_b2.update())
    newDataReady = true;
  if (LoadCell_g.update())
    newDataReady = true;
  if (LoadCell_b3.update())
    newDataReady = true;
  if (LoadCell_b4.update())
    newDataReady = true;

  // Get smoothed value from data set
  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
      float bottle1 = LoadCell_b1.getData();
      float bottle2 = LoadCell_b2.getData();
      float bottle3 = LoadCell_b3.getData();
      float bottle4 = LoadCell_b4.getData();
      float glass = LoadCell_g.getData();

      if(initialized >= 5) {
        Serial.println("{\"b1\": " + String(bottle1) + ", \"b2\": " + String(bottle2) + ", \"b3\": " + String(bottle3) + ", \"b4\": " + String(bottle4) + ", \"g\": " + String(glass) + "}");
        newDataReady = 0;
        t = millis();
      }
    }
  }

  // Receive command from serial terminal, send [1-5] to initiate tare operation
  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == '1') {
      LoadCell_b1.tareNoDelay(); // tare load cell for bottle 1
    } else if (inByte == '2') {
      LoadCell_b2.tareNoDelay(); // tare load cell for bottle 2
    } else if (inByte == '3') {
      LoadCell_b3.tareNoDelay(); // tare load cell for bottle 3
    } else if (inByte == '4') {
      LoadCell_b4.tareNoDelay(); // tare load cell for bottle 4
    } else if (inByte == '5') {
      LoadCell_g.tareNoDelay();  // tare load cell for glass
    }
  }

  // Check if last tare operation is complete
  if (LoadCell_b1.getTareStatus() == true) {
    initialized += 1;
    Serial.println("Tare load cell 1 complete");
  }
  if (LoadCell_b2.getTareStatus() == true) {
    initialized += 1;
    Serial.println("Tare load cell 2 complete");
  }
  if (LoadCell_b3.getTareStatus() == true) {
    initialized += 1;
    Serial.println("Tare load cell 3 complete");
  }
  if (LoadCell_b4.getTareStatus() == true) {
    initialized += 1;
    Serial.println("Tare load cell 4 complete");
  }
  if (LoadCell_g.getTareStatus() == true) {
    initialized += 1;
    Serial.println("Tare load cell 5 complete");
  }
}
