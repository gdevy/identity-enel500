#include <SPI.h>
#include <SD.h>

File myFile;
unsigned long t=0;
void setup()
{
    // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    while (1);
  }

}
void loop()
{
   myFile = SD.open("N.txt");
   delay(250);
      int userInput = Serial.read();



      
  if(userInput == 'G')//////////////////////////////////////
  { ////////////////////////////////////////////////////////
  if (myFile) {  
    // read from the file until there's nothing else in it:
    while (myFile.available()) 
    {
      myFile.read();
      t++;
    }
    Serial.print(t);
    // close the file:
    myFile.close();
       while(1)
      ;
  }
  else {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt111111111");
    while(1)
      ;
   }

   
 }/////////////////////////////////////////////////////
  
  
  
}
