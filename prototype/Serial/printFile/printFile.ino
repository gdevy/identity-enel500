#include <SPI.h>
#include <SD.h>
char a;
File myFile;
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
  if (myFile) {
     int userInput1 = Serial.read(); 
  if(userInput1 == 'g')///////////////////////////////////////
  {//////////////////////////////////////////////////////////  
    // read from the file until there's nothing else in it:
    int i=1;
    while(i<=162){
    String x="";
    a=myFile.read();
    while (a!='\n') {  
      x=x+a;
      a=myFile.read();
    }
     Serial.println(x);
     i++;
    }
    // close the file:
    myFile.close();
    while(1)
      ;

   }//////////////////////////////////////////////////////
  }
     else {
    // if the file didn't open, print an error:
    Serial.println("error opening test.txt2222222");
    while(1)
      ;
   }
  
}
