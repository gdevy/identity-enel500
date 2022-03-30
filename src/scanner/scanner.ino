////////////////////////////////////////////////////////////////////////////////////////////////////////
//            SCANNER CONNECTION
//  NFC READER                    Arduino Uno
//  SDA              ->           PIN 10
//  SCL              ->           PIN 13
//  MOSI             ->           PIN 11
//  MISO             ->           PIN 12
//  IRQ              ->           OPEN
//  GND              ->           GND
//  RST              ->           PIN 5
//  3.3V             ->           3.3V
//
//  MASTER BLUETOOTH
//                      2k ohm -> GND
//  KEY(EN)          -> | (3.3V)
//                      1k ohm <- PIN 4
//  VCC              ->           PIN 8
//  GND              ->           GND
//  TXD              ->           PIN 3
//                      2k ohm -> GND
//  RXD              -> | (3.3V)
//                      1k ohm <- PIN 2
//  STATE            ->           OPEN
//
////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <SPI.h>          //include the SPI bus library
#include <MFRC522.h>      //include the RFID reader library
#include <NeoSWSerial.h>  //include the NeoSWSerial library for serial communication

#define NFC_SS_PIN 10  //slave select pin
#define NFC_RST_PIN 5  //reset pin
#define EN_PIN 4       //Bluetooth enable pin
#define PW_PIN 8       //Bluetooth power pin
#define BT_TX 2        //TX pin
#define BT_RX 3        //RX pin

MFRC522 mfrc522(NFC_SS_PIN, NFC_RST_PIN);  // instatiate a MFRC522 reader object.
MFRC522::MIFARE_Key key;          //create a MIFARE_Key struct named 'key', which will hold the card information

NeoSWSerial configBt(BT_RX, BT_TX); // RX, TX

int stage_one = 0;
int stage_two = 0;
int stage_three = 0;
int block = 2;

byte blockcontent[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
byte zeroblock[16]   = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
byte str[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
byte btest[3];              // used to store reponse from bluetooth module

//This array is used for reading out a block.
byte readbackblock[18];

String test;

void setup() {
  Serial.begin(9600);   // Initialize serial communications with the PC
  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  // init SPI
  SPI.begin();

  // Init MFRC522
  mfrc522.PCD_Init();
  delay(4);       // Optional delay. Some board do need more time after init to be ready, see Readme
  // mfrc522.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details

  pinMode(BT_TX, OUTPUT);
  pinMode(BT_RX, INPUT);
  pinMode(EN_PIN, OUTPUT);
  pinMode(PW_PIN, OUTPUT);

  digitalWrite(PW_PIN, LOW); // power off
  digitalWrite(EN_PIN, LOW); // enable off

  // Prepare the security key for the read and write functions.
  for (byte i = 0; i < 6; i++)
  {
    key.keyByte[i] = 0xFF;  //keyByte is defined in the "MIFARE_Key" 'struct' definition in the .h file of the library
  }

  //start check----------------------------------
  // Exit the loop until got "start" from PC
  while (1) {
    if (Serial.available()) {
      String startflag = Serial.readStringUntil('\n'); // Reading anything from PC
      if (startflag == "start") {
        Serial.println("ok");
        break;
      }
    }
  }
  //---------------------------------------------
}

void loop() {

  NFC_Reading(); // scan an NFC tag to obtain Bluetooth addresses (stage 1)

  if (stage_one == 1) {
    // setting up BT connection (stage 2)
    debugMessage("NFC tag was read.");
    BLE_Setup();
    Serial.flush();
  }

  if (stage_two == 1) {
    // Recieve template and send it (stage 3)
    debugMessage("BLE is updated.");
    // communite with passport
    delay(10);
    receiveTemplate();
    Serial.flush();
  }
}

//Scan NFC tag
void NFC_Reading() {

  debugMessage("Scan a MIFARE Classic card");

  while (1) {
    //   Look for new cards
    if (mfrc522.PICC_IsNewCardPresent()) {
      break;
    }
  }

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  debugMessage("NFC card detected");

  //read the block back
  readBlock(block, readbackblock);

  for (int i = 0; i < 16; i++) {
    if (readbackblock[i] != zeroblock[i]) {
      stage_one = 1;
      str[i] = readbackblock[i];
    }
  }

  String address((char*) readbackblock);
  String read_message = "read block: ";
  debugMessage(read_message + address);
  reselect_Card();
  //mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
}

// from
// https://stackoverflow.com/questions/62171216/mfrc-522-authentication-reset-on-arduino-ide-with-esp32
bool reselect_Card() {
  //-------------------------------------------------------
  // Can also be used to see if card still available,
  // true means it is false means card isnt there anymore
  //-------------------------------------------------------
  byte s;
  byte req_buff[2];
  byte req_buff_size = 2;
  mfrc522.PCD_StopCrypto1();
  s = mfrc522.PICC_HaltA();
  // Serial.print("Halt Status: ");
  // Serial.println(mfrc522.GetStatusCodeName((MFRC522::StatusCode)s));
  delay(100);
  s = mfrc522.PICC_WakeupA(req_buff, &req_buff_size);
  // Serial.print("Request: ");
  // Serial.println(mfrc522.GetStatusCodeName((MFRC522::StatusCode)s));
  // Serial.print("ATQA : ");
  //Serial.println(dump_byte_array_to_string(req_buff,req_buff_size));
  delay(100);
  s = mfrc522.PICC_Select( &(mfrc522.uid), 0);
  // Serial.print("Selected : ");
  // Serial.println(mfrc522.GetStatusCodeName((MFRC522::StatusCode)s));
  if ( mfrc522.GetStatusCodeName((MFRC522::StatusCode)s) == F("Timeout in communication.") ) {
    return false;
  }
  return true;
}


//Set up Bluetooth module pairing

////////////////////////////////////////////////////////////////////////////////
void BLE_Setup() {

  int sent = 0;

  stage_one = 0;

  digitalWrite(EN_PIN, HIGH);// enable pin high
  digitalWrite(PW_PIN, HIGH);// power on



  configBt.begin(38400);//setting rate for conmunicating BLE module
  delay(2000);


  configBt.println("AT");    //necessery to clear first-time error
  delay(30);
  configBt.println("AT");
  delay(30);
  parseBTResponse();
  delay(500);
  //------------------------

  int retries = 0;
  bool match = false;

  while (!match) {//exit when got 3 "ok" which means Bluetooth module is setup
    String bt_loop_message = "BT setup loop: ";
    debugMessage(bt_loop_message + retries);
    //Exit setup loop if it fails to setup for 3 times
    if (retries >= 3) {
      match = false; //Error mark
      break;
    }

    //Set role for Bluetooth module (1 for "master"; 0 for "slave")
    bool role_ok = false;
    configBt.println("AT+ROLE=1");
    role_ok = parseBTResponse();

    String role_ok_message = "BT role set: ";
    debugMessage(role_ok_message + role_ok);

    //Set communication mode for Bluetooth module (0 for "connect to a fixed address"; 1 for "connect to any address")
    bool bt_mode = false;
    configBt.println("AT+CMODE=0");
    bt_mode = parseBTResponse();

    String mode_ok_message = "BT role set: ";
    debugMessage(mode_ok_message + bt_mode);

    //Set the fixed address that Bluetooth module should connected to
    bool bt_address_set = false;
    configBt.print("AT+BIND=");
    str[14] = 13;
    str[15] = 10;
    configBt.write(str, 16);
    bt_address_set = parseBTResponse();

    String address_set_message = "BT address set: ";
    debugMessage(address_set_message + bt_address_set);

    retries += 1;
    match = role_ok && bt_mode && bt_address_set;
  }

  String stage_2_end_message = "Stage 2 complete status: ";
  debugMessage(stage_2_end_message + match);

  //Set mark to enter stage 3 if Bluetooth module is set up
  if (match) {
    stage_two = 1;
  }

  delay(100);

  configBt.flush();

  //Bluetooth module needs to be restart for tranferring template
  digitalWrite(PW_PIN, LOW);// power off
  delay(100);
  digitalWrite(EN_PIN, LOW);// enable pin low
  digitalWrite(PW_PIN, HIGH);// power on
  delay(100);
}

void debugMessage(String message) {
  String command = "print ";
  Serial.println(command + message.length());
  Serial.println(message);
}

bool parseBTResponse() {
  delay(300);
  if (configBt.available()) { //if the bluetooth module is sending something...
    test = configBt.readString(); //print whatever the bluetooth module is sending
  }

  //debug info
  String bt_response_message = "BT response: ";
  debugMessage(bt_response_message + test);

  //change string to a byte array
  test.getBytes(btest, 3);

  //Compare massage from Bluetooth module with "ok"
  int matched = 0;
  byte okbyte[2] = {79, 75};   // "ok" in byte format
  for (int i = 0; i < 2; i++) {
    if (btest[i] == okbyte[i]) {
      matched += 1;
    }
  }

  return matched == 2;
}

//Recieve template file
void receiveTemplate() {

  digitalWrite(EN_PIN, LOW); // enable pin low
  //digitalWrite(PW_PIN,LOW);// power off
  digitalWrite(PW_PIN, HIGH); // power on

  configBt.begin(9600);
  delay(500);

  bool at_start = false;

  //  byte template_buffer[128];
  int template_idx = 0;
  String fname, lname, dob, template_buffer;
  while (1) {
    if (configBt.available()) {
      byte character = configBt.read();
      if (character == '@') {
        break;
      }
    }
  }

  fname = configBt.readStringUntil('\n');
  lname = configBt.readStringUntil('\n');
  dob = configBt.readStringUntil('\n');
  template_buffer = configBt.readStringUntil('@');
  String info_message = template_buffer;

  String temp  = "info ";
  String info_command_message = temp + fname.length() + " " + lname.length() + " " + dob.length();
  Serial.println(info_command_message);
  Serial.println(fname);
  Serial.println(lname);
  Serial.println(dob);

  String template_message = template_buffer;
  //  String info_message = String((char*)template_buffer);
  temp  = "template ";
  String template_command_message = temp + sizeof(template_buffer) + " " + sizeof(template_buffer);
  Serial.println(template_command_message);
  Serial.print(template_message);

  while (1) {
    if (Serial.available()) {
      String doneflag = Serial.readStringUntil('\n'); // Reading anything from PC
      if (doneflag == "auth yes" || doneflag == "auth no") {
        stage_one = 0;
        stage_two = 0;
        stage_three = 0;
        Serial.println("");
        Serial.print("STAGE 3 Done");
        break;
      }
      else {
        stage_one = 0;
        stage_two = 0;
        stage_three = 0;
        Serial.println("");
        Serial.print("Unexpected error");
        break;
      }
    }
  }

  digitalWrite(PW_PIN, LOW); // power off
}

//Read specific block
int readBlock(int blockNumber, byte arrayAddress[]) {
  int largestModulo4Number = blockNumber / 4 * 4;
  int trailerBlock = largestModulo4Number + 3; //determine trailer block for the sector

  //authentication of the desired block for access
  byte status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));

  if (status != MFRC522::STATUS_OK) {
    String failed_message_3 = "PCD_Authenticate() failed (read): ";
    //debugMessage( "PCD_Authenticate() failed (read): " + mfrc522.GetStatusCodeName(status));
    return 3;//return "3" as error message
  }

  //reading a block
  byte buffersize = 18;//we need to define a variable with the read buffer size, since the MIFARE_Read method below needs a pointer to the variable that contains the size...
  status = mfrc522.MIFARE_Read(blockNumber, arrayAddress, &buffersize);//&buffersize is a pointer to the buffersize variable; MIFARE_Read requires a pointer instead of just a number
  if (status != MFRC522::STATUS_OK) {
    String failed_message_4 = "MIFARE_read() failed: ";
    //debugMessage(failed_message_4 + mfrc522.GetStatusCodeName(status);
    return 4;//return "4" as error message
  }
}
