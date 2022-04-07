Before import passport code, please setup NFC tag first.

To setup tag:

1.Obtain passport (slave) Bluetooth module address.

***Resistors will be used (as voltage divider) to provide 3.3V (required) voltage to RXD pin on Bluetooth module.
***Exceed 3.3V too much could damage the module, and module may not working if voltage is below to much. 
***There will be two sets of resistors to provide 3.3V in our design (passport and scanner).
***Because Arduino nano digital pin (e.g. D2) provide different voltage when powered by usb port(4.7V) and by our designed battery(4.2V)
***You can any resistor to provide 3.3V but please test the output before connecting to the module. 

1.1 If Bluetooth module is not connected to motherboard(when resistors were not set for battery).
1.1.1 For HC-06 
1.1.1.1 By Arduino IDE
Connect the module to Arduino nano board. 
Make sure USB port is providing power to Arduino.
(Vcc to 5V pin, GND to GND, D2 to 1k ohms resistor to 2k ohms resistor to GND and RXD to the middle of resistors, TXD to D3)
Upload "manualBLEsetup" code to Ardunio.
Open Arduino IDE.
Select "port" under "Tools".
Open "Serial Monitor" under same submenu.
Set serial monitor to "Both NL & CR" and "9600 baud"
Input "AT" first, then you should get "error(0)" or "OK"
Then input "AT+ADDR?"
1.1.1.2 By phone
If HC-06 does not response to any AT command, you can use phone to obtain address
Connect the module to Arduino nano board. 
Make sure USB port is providing power to Arduino.
(Vcc to 5V pin, GND to GND, D2 to 1k ohms resistor to 2k ohms resistor to GND and RXD to the middle of resistors, TXD to D3)
The Bluetooth Module LED should be blinking very fast
Make sure you have a serial terminal app installed on phone (e.g. "Serial Bluetooth Terminal")
Turn on Bluetooth on phone
Connect to "HC-05" or device with similar name 
Password is 1234 or 0000 if required
Open terminal, check device, you should see address
1.1.2 For HC-05
1.1.2.1 By Arduino IDE 
Same as 1.1.1.1 but have EN pin of HC-05 connects to D5
1.1.2.2 By phone
Same as 1.1.1.2

2. Rewrite Bluetooth Address
Depend on method you used, you may have different address in different format
Convert them into "XXXX,XX,XXXXXX"
e.g. 1  "14:3:508b2"        -> "0014,03,0508b2"
e.g. 2  "00:14:03:05:59:6D" -> "0014,03,05596D"

3. Write tag
Open "RFID_write" code in Arduino IDE
replace variable "blockcontent" with the converted address
Upload "RFID_write" code to Arduino board

Then the tag is setup

