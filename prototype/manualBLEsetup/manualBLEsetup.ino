//  SLAVE BLUETOOTH               Arduino nano
//  KEY(EN)          ->           D5   
//  VCC              ->           5V
//  GND              ->           GND
//  TXD              ->           D3
//                                2k ohm -> GND
//  RXD              ->           | (3.3V)        (assuming power is provided by USB port)
//                                1k ohm <- D2
//  STATE            ->           OPEN

#include <NeoSWSerial.h>

#define EN_PIN 5  //Bluetooth enable pin
#define BT_TX 2
#define BT_RX 3

NeoSWSerial configBt(BT_RX, BT_TX); // RX, TX

void setup() {
  Serial.begin(9600);
  configBt.begin(38400);
  pinMode(BT_TX, OUTPUT);
  pinMode(BT_RX, INPUT);
  digitalWrite(EN_PIN,HIGH);// enable pin high
}

void loop() {
  
  if(configBt.available()) //if the bluetooth module is sending something...
  {
    Serial.print(configBt.readString()); //print whatever the bluetooth module is sending 
  }

  if(Serial.available()) //if we have typed anything into the serial monitor input text box...
  {
    Serial.print(Serial.peek());
    configBt.write(Serial.read()); //write whatever we typed into the serial monitor input text box to the bluetooth module
  }

}
