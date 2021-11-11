import serial
import time
from cryptography.fernet import Fernet
x=0
attempt=1
key = b'wWGAOCPMXdL2hcgllfjwz4fu0L_2gUtDMox36UiHNBw='
crypter = Fernet(key)
while(1):
    a=[]
    b=[]
    try:
        ser = serial.Serial('/dev/cu.usbmodem14201', baudrate=9600, timeout=1)
        if x==1:
            continue
    except Exception:
        x=0
        continue
    try:
        print("---------------------------------------------")
        print("Attempt "+str(attempt))
        rawdata = []
        time.sleep(2)
        ser.write(b'g')
        time.sleep(2)
        i = 0
        while i < 162:
            rawdata = str(ser.readline())
            a.append(rawdata[2:-5])
            i = i + 1

        i = 0
        while i < 162:
            b.append(str(crypter.decrypt(str.encode(a[i])), 'utf8'))
            i = i + 1

        i = 0
        while i < 162:
            print(b[i])
            i = i + 1
        x=x+1
        print("Attempt "+str(attempt)+" was successful")
        print("---------------------------------------------")
        attempt=attempt+1
    except Exception:
        print("Attempt "+str(attempt)+" was not successful")
        print("---------------------------------------------")
        attempt=attempt+1
        continue
