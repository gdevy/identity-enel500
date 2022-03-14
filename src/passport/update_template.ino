#include <SPI.h>
#include <SD.h>
#define SD_PIN 10

File myFile;

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  Serial.print("Initializing SD card...");

  if (!SD.begin(SD_PIN)) {
    Serial.println("initialization failed!");
    while (1);
  }
  Serial.println("initialization done.");

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  myFile = SD.open("test.txt", FILE_WRITE);

  // if the file opened okay, write to it:
  if (myFile) {
    while(1){
      if(Serial.available()){
        String startflag = Serial.readString(); // Reading anything from PC
        if(startflag == "start"){
          Serial.println("OK");
          debugMessage("Start writing to SD card");
          break;
        }
      }
    }
    while(Serial.available()){       
        char character = (char)Serial.read();
        myFile.print(character);
    }
    // close the file:
    myFile.close();
    debugMessage("done.");
  } else {
    // if the file didn't open, print an error:
    debugMessage("error opening test.txt");
  }

  // re-open the file for reading:
  myFile = SD.open("test.txt");
  if (myFile) {
    debugMessage("test.txt:");

    // read from the file until there's nothing else in it:
    while (myFile.available()) {
      debugMessage(myFile.read());
    }
    // close the file:
    myFile.close();
  } else {
    // if the file didn't open, print an error:
    debugMessage("error opening test.txt");
  }
}

void loop() {
  // nothing happens after setup
}

void debugMessage(String message) {
  String command = "print ";
  Serial.println(command + message.length());
  Serial.println(message);
}
