import serial
import time


def clean(L):
    newl = []
    for i in range(len(L)):
        temp = L[i][2:]
        newl.append(temp[:-6])
    return newl


count = 0
ser = serial.Serial('/dev/cu.usbmodem14101', baudrate=9600, timeout=1)
rawdata = []
time.sleep(2)
ser.write(b'g')
time.sleep(2)
i = 1
while i <= 162:
    rawdata = str(ser.readline())
    print(rawdata[2:-7])
    i = i + 1
