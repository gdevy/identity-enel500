import serial
import time


def clean(L):
    newl = []
    for i in range(len(L)):
        temp = L[i][2:]
        newl.append(temp[:-6])
    return newl


g = 0
ser = serial.Serial('/dev/cu.usbmodem14101', baudrate=9600, timeout=1)
rawdata = []
count = 0
time.sleep(1)
ser.write(b'G')
time.sleep(2)
A = str(ser.readline())
print(A)
j = int(A[2:-1])
print(j)
