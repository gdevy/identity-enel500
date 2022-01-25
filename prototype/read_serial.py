import serial

with serial.Serial('COM5', 9600, timeout=1) as ser:
    # x = ser.read()  # read one byte
    # s = ser.read(10)  # read up to ten bytes (timeout)
    while True:
        print(ser.readline())  # read a '\n' terminated line
