////////////////////////////////////////////////////////////////////////////////////////////////////////
//            PASSPORT CONNECTION 
//  SD CARD READER                Arduino Nano
//  CS               ->           D10
//  SCK              ->           D13
//  MOSI             ->           D11
//  MISO             ->           D12
//  VCC              ->           5V
//  GND              ->           GND
//
//  SLAVE BLUETOOTH          
//  KEY(EN)          ->           D13
//  VCC              ->           5V
//  GND              ->           GND
//  TXD              ->           D3
//                      2k ohm -> D2
//  RXD              -> | (3.3V)
//                      1k ohm <- 5V
//  STATE            ->           OPEN
//
////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <NeoSWSerial.h>
#include <SPI.h>
#include <SD.h>

#define BT_TX 2
#define BT_RX 3
#define SD_PIN 10

File TEMPLATE;
NeoSWSerial configBt(BT_RX, BT_TX); // RX, TX

void setup() {
  Serial.begin(9600); 
  configBt.begin(9600); 
  pinMode(BT_TX, OUTPUT); 
  pinMode(BT_RX, INPUT); 
  pinMode(SD_PIN, OUTPUT); // chip select pin must be set to OUTPUT mode
  if (!SD.begin(SD_PIN)) { // Initialize SD card
    debugMessage("Could not initialize SD card."); // if return value is false, something went wrong.
  }
  if (SD.exists("TEMPLATE.txt")) { // Check whether "TEMPLATE.txt" exists
    debugMessage("TEMPLATE exists.");
  }
}

void loop() {
  char test;

  TEMPLATE = SD.open("TEMPLATE.txt", FILE_READ); // open "TEMPLATE.txt" to read data
  if (TEMPLATE) {
    debugMessage("- – Reading start – -");
    char character;
    while ((character = TEMPLATE.read()) != -1) { // this while loop reads data stored in "TEMPLATE.txt" and prints it to serial monitor
      configBt.print(character);
    }
    TEMPLATE.close();
    configBt.print('@');
    debugMessage("- – Reading end – -");
  } else {
    debugMessage("Could not open file (reading).");
  }
  delay(500); // wait for 500ms

}

void debugMessage(String message) {
  String command = "print ";
  Serial.println(command + message.length());
  Serial.println(message);
}
