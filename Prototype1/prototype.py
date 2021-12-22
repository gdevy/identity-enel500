import serial
import time
import cv2
import face_recognition
import numpy
import copy
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
        ser.write(b'g')
        i = 0
        while i < 128:
            rawdata = str(ser.readline())
            a.append(rawdata[2:-5])
            b.append(float(str(crypter.decrypt(str.encode(a[i])), 'utf8')))
            i = i + 1
        x=x+1
        my_array = numpy.array(b)
        # Take a picture with the webcam and convert that image to a template
        
        
        a = 0
        i = 1
        name = "Look at the camera and make sure your whole face is in the frame"
        cam = cv2.VideoCapture(0)
        start = time.time()
        while time.time() - start < 5:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            #----------
            frame1 = copy.deepcopy(frame)
            cv2.putText(frame1, name, (7, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imshow("temp", frame1)
            cv2.waitKey(1)
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            raise
        #----------
        frame1 = copy.deepcopy(frame)
        cv2.putText(frame1, name, (7, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.imshow("temp", frame1)
        #-----------
        cv2.imwrite("temp.jpeg", frame)
        test_image = face_recognition.load_image_file("temp.jpeg")
        face_locations = face_recognition.face_locations(test_image)
        top, right, bottom, left = face_locations[0]
        face_image = frame[top:bottom, left:right]
        cv2.imwrite("1.jpeg", face_image)
        cam.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        image2=face_recognition.load_image_file("1.jpeg")
        image2_face_encoding=face_recognition.face_encodings(image2)[0]
        # Compare the two templates
        results=face_recognition.compare_faces([my_array], image2_face_encoding)
        if results[0]:
            print("The Faces Match")
        else:
            print("The Faces do not Match")
        print("---------------------------------------------")
        attempt=attempt+1
    except Exception:
        print("Attempt "+str(attempt)+" was not successful")
        print("---------------------------------------------")
        attempt=attempt+1
        continue
