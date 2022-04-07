Before import passport code, please setup NFC tag first.

To setup tag:

1.Obtain passport (slave) Bluetooth module address.

***Resistors will be used (as voltage divider) to provide 3.3V (required) voltage to RXD pin on Bluetooth module.
***Exceed 3.3V too much could damage the module, and module may not working if voltage is below to much. 
***There will be two sets of resistors to provide 3.3V in our design (passport and scanner).
***Because Arduino nano digital pin (e.g. D2) provide different voltage when powered by usb port(4.7V) and by our designed battery(4.2V)
***You can any resistors to provide 3.3V but please test the output before connecting to the module. 

1.1 If Bluetooth module is not connected to motherboard(when resistors were not set for battery).
1.1.1 For HC-06 
1.1.1.1 By Arduino IDE
Connect the module to Arduino nano board. 
Make sure USB port is providing power to Arduino.
(Vcc to 5V pin, GND to GND, D2 to 1k ohms resistor to 2k ohms resistor to GND and RXD to the middle of resistors, TXD to D3)
Import "manualBLEsetup" to Ardunio.
Open Arduino IDE.
Select "port" under "Tools".
Open "Serial Monitor" under same submenu.

