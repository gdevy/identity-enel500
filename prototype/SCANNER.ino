#include <SPI.h>      //include the SPI bus library
#include <MFRC522.h>  //include the RFID reader library
#include <NeoSWSerial.h>

#define NFC_SS_PIN 10  //slave select pin
#define NFC_RST_PIN 5  //reset pin
#define EN_PIN 4  //Bluetooth enable pin
#define PW_PIN 8   //Bluetooth power pin
#define BT_TX 2
#define BT_RX 3

MFRC522 mfrc522(NFC_SS_PIN, NFC_RST_PIN);  // instatiate a MFRC522 reader object.
MFRC522::MIFARE_Key key;          //create a MIFARE_Key struct named 'key', which will hold the card information

NeoSWSerial configBt(BT_RX, BT_TX); // RX, TX

int stage_one = 0;
int stage_two = 0;
int stage_three = 0;
int block = 2;

byte blockcontent[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
byte zeroblock[16]   = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
byte str[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

//This array is used for reading out a block.
byte readbackblock[18];

void setup() {
    Serial.begin(9600);   // Initialize serial communications with the PC
    while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

    // init SPI
    SPI.begin();

    // Init MFRC522
    mfrc522.PCD_Init();
    delay(4);       // Optional delay. Some board do need more time after init to be ready, see Readme
    mfrc522.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details

    pinMode(BT_TX, OUTPUT);
    pinMode(BT_RX, INPUT);
    pinMode(EN_PIN, OUTPUT);
    pinMode(PW_PIN,OUTPUT);

    // Prepare the security key for the read and write functions.
    for (byte i = 0; i < 6; i++)
    {
      key.keyByte[i] = 0xFF;  //keyByte is defined in the "MIFARE_Key" 'struct' definition in the .h file of the library
    }

    Serial.println("Scan a MIFARE Classic card");
}

void loop() {

    if (stage_one == 0) {       // waiting for NFC tag
        NFC_Reading();
    }

    if (stage_one == 1) {       // setting up BT connection
        Serial.print("NFC tag was read.");
        BLE_Setup();
    }

    if (stage_two == 3) {       // sending info
        Serial.print("BLE is updated.");
        // communite with passport
        delay(100);
        File_update();
    }
}

  //Scan NFC tag
void NFC_Reading() {
    //   Look for new cards
    if (!mfrc522.PICC_IsNewCardPresent()) {
        return;
    }

    // Select one of the cards
    if (!mfrc522.PICC_ReadCardSerial()) {
        return;
    }
    Serial.println("card selected");

    //read the block back
    readBlock(block, readbackblock);

    for (int i=0; i<16; i++) {
        if (readbackblock[i] != zeroblock[i]) {
            stage_one = 1;
            str[i] = readbackblock[i];
        }
    }

    //print the block contents
    Serial.print("read block: ");
    for (int j=0 ; j<16 ; j++) {
        Serial.write(readbackblock[j]);
    }
    Serial.println("");

    Serial.print("read block: ");
    for (int j=0 ; j<16 ; j++) {
        Serial.write (str[j]);
    }
    Serial.println("");

    mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
}

  //Set up Bluetooth module pairing

////////////////////////////////////////////////////////////////////////////////
void BLE_Setup() {
    digitalWrite(PW_PIN,LOW);// power off
    // press button
    digitalWrite(EN_PIN,HIGH);// enable pin high
    digitalWrite(PW_PIN,HIGH);// power on
    // release button

    configBt.begin(38400);

    delay(200);//Wait for Bluetooth to turn on

    do {
        if (configBt.available()) { //if the bluetooth module is sending something...
            Serial.print(configBt.readString()); //print whatever the bluetooth module is sending
        }

        //master setting
        configBt.println("AT");
        delay(30);
        configBt.println("AT");
        delay(30);
        configBt.println("AT+ROLE=1");
        delay(30);
        configBt.println("AT+ROLE?");
        delay(30);
        configBt.println("AT+CMODE=0");
        delay(30);
        configBt.println("AT+CMODE?");
        delay(30);
        configBt.print("AT+BIND=");
        str[14] = 13;
        str[15] = 10;
        configBt.write(str,16);
        delay(30);
        configBt.println("AT+BIND?");
        delay(30);

        stage_two += 1;

    } while (stage_two != 3);

    //delay(100);

    digitalWrite(PW_PIN,LOW);// power off
    digitalWrite(EN_PIN,LOW);// enable pin low
    digitalWrite(PW_PIN,HIGH);// power on
}

//Recieve template file
void File_update() {
    stage_one = 0;
    stage_two = 0;
    stage_three = 0;
}

//Read specific block
int readBlock(int blockNumber, byte arrayAddress[]) {
    int largestModulo4Number=blockNumber/4*4;
    int trailerBlock=largestModulo4Number+3;//determine trailer block for the sector

    //authentication of the desired block for access
    byte status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));

    if (status != MFRC522::STATUS_OK) {
         Serial.print("PCD_Authenticate() failed (read): ");
         Serial.println(mfrc522.GetStatusCodeName(status));
         return 3;//return "3" as error message
    }

    //reading a block
    byte buffersize = 18;//we need to define a variable with the read buffer size, since the MIFARE_Read method below needs a pointer to the variable that contains the size...
    status = mfrc522.MIFARE_Read(blockNumber, arrayAddress, &buffersize);//&buffersize is a pointer to the buffersize variable; MIFARE_Read requires a pointer instead of just a number
    if (status != MFRC522::STATUS_OK) {
          Serial.print("MIFARE_read() failed: ");
          Serial.println(mfrc522.GetStatusCodeName(status));
          return 4;//return "4" as error message
    }
    Serial.println("block was read");
}
