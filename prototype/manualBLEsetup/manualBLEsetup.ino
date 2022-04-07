//  SLAVE BLUETOOTH               Arduino nano
//  KEY(EN)          ->           D5   
//  VCC              ->           5V
//  GND              ->           GND
//  TXD              ->           D3
//                                2k ohm -> GND
//  RXD              ->           | (3.3V)        (assuming power is provided by USB port)
//                                1k ohm <- D2
//  STATE            ->           OPEN

//
// For testing, the serial monitor should be set to "Both NL & CR" and "9600 baud"
// The Bluetooth module should be flashing with about 1s period
// If not, disconnect 5V pin with usb cable connected and then connect 5V pin again 
// For Master Module: Input "AT" then "AT+ROLE=1" then "AT+CMODE=0"
// For Slave  Module: Input "AT" then "AT+ROLE=0" then "AT+CMODE=1"
// To find the address: Input "AT+ADDR?"
// For more AT commands, please refer to HC-05 AT Command Set: https://s3-sa-east-1.amazonaws.com/robocore-lojavirtual/709/HC-05_ATCommandSet.pdf
// Or google "HC-05 AT Command"

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
  pinMode(EN_PIN,OUTPUT);
  delay(100);
  digitalWrite(EN_PIN,HIGH);// enable pin high
  
}

void loop() 
{
  if(configBt.available()) // if the HC05 is sending something… 
  {
    Serial.print(configBt.readString()); // print in serial monitor
  }
  if(Serial.available()) // if serial monitor is outputting something… 
  {
    configBt.write(Serial.read()); // write to Arduino’s Tx pin
  }
}
