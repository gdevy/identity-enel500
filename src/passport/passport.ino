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
//  KEY(EN)          ->           D5   (is open when hc-06 is used)
//  VCC              ->           5V
//  GND              ->           GND
//  TXD              ->           D3
//                      2k ohm -> GND
//  RXD              -> | (3.3V)
//                      1k ohm <- D2
//  STATE            ->           OPEN
//
//  Battery Check
//  Pin A4           ->           Battery (+)  
//  Pin 8            ->           LED Resistor       ->      LED
//
////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <NeoSWSerial.h>
// #include <SPI.h>
#include <SD.h>

#define BT_TX 2
#define BT_RX 3
#define SD_PIN 10
#define Bat_PIN A4
#define LED_PIN 8
#define EN_PIN 5


File Template;
char* TEMPLATEFILE = "TEMPLATE.txt";

NeoSWSerial configBt(BT_RX, BT_TX); // RX, TX

void setup() {
  Serial.begin(9600); 
  configBt.begin(9600);

  pinMode(BT_TX, OUTPUT); 
  pinMode(BT_RX, INPUT); 
  pinMode(SD_PIN, OUTPUT); // chip select pin must be set to OUTPUT mode
  //pinMode(Bat_PIN,INPUT);   // pc1
  //pinMode(LED_PIN,OUTPUT);  // pc2
  //pinMode(EN_PIN,OUTPUT);   // hc1

  //hc05_setup();  //uncomment hc1 and this function when hc-05 is used
  //power_check(); //uncomment pc1, pc2 and this function to warn user when battery is low
  
  if (!SD.begin(SD_PIN)) { // Initialize SD card
    debugMessage("Could not initialize SD card."); // if return value is false, something went wrong.
    return 1;
  }

  if (!SD.exists("TEMPLATE.txt")) { // Check whether "TEMPLATE.txt" exists
    debugMessage("Template file not found exists.");
    return 1;
  }

  Template = SD.open("TEMPLATE.txt", FILE_READ); // open template file to read data

  if (!Template) {
    debugMessage("Couldn't open template file");
    return 1;
  }

}

void loop() {

    debugMessage("- – Reading start – -");

    char character;
    while ((character = Template.read()) != -1) { // this while loop reads data stored in "TEMPLATE.txt" and prints it to serial monitor
        configBt.print(character);
    }

    configBt.print('@');
    Template.seek(0);
    debugMessage("- – Reading end – -");

  delay(500); // wait for 500ms

}

void power_check(){
  double vol = (analogRead(Bat_PIN)/1024.0)*5.0;
  if(vol < 4.08){ //this is 3.8V 
    digitalWrite(LED_PIN,HIGH); 
    delay(1000);
    digitalWrite(LED_PIN,LOW); 
  }
}

void hc05_setup(){
  configBt.begin(38400);
  digitalWrite(EN_PIN,HIGH);
  
  configBt.println("AT");    //necessery to clear first-time error
  delay(30);
  configBt.println("AT");
  delay(30);
  
  configBt.println("AT+ROLE=0"); //Set role for Bluetooth module (1 for "master"; 0 for "slave")
  delay(30);
  configBt.println("AT+CMODE=1"); //Set communication mode for Bluetooth module (0 for "connect to a fixed address"; 1 for "connect to any address")
  delay(30);

  configBt.begin(9600);
  digitalWrite(EN_PIN,LOW);
}

void debugMessage(String message) {
  String command = "print ";
  Serial.println(command + message.length());
  Serial.println(message);
}
