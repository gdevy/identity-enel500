import serial

# with serial.Serial('COM5', 9600, timeout=1) as ser:
#     # x = ser.read()  # read one byte
#     # s = ser.read(10)  # read up to ten bytes (timeout)
#     while True:
#         print(ser.readline())  # read a '\n' terminated line
#

if __name__ == '__main__':
    with serial.Serial("COM5", 9600) as port:
        command_in = port.readline()

    command, *args = command_in.split()

    if command == "template":
        num_bytes = args[0]

        with serial.Serial("COM5", 9600) as port:
            bytes_in = port.read(num_bytes)

        print(f"read {len(bytes_in)} bytes")
        print(bytes_in)
