import serial
import time
import cv2
import face_recognition
import numpy
import copy

x=0
attempt=1
while(1):
    a=[]
    b=[]
    try:
        ser = serial.Serial('/dev/cu.usbmodem14201', baudrate=115200, timeout=1)
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
            b.append(float(a[i]))
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
            frame_withText = copy.deepcopy(frame)
            cv2.putText(frame_withText, name, (7, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imshow("temp", frame_withText)
            cv2.waitKey(1)
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            raise
        cv2.imwrite("temp.jpeg", frame) # this line is only for debugging (optional)
        face_locations = face_recognition.face_locations(frame)
        top, right, bottom, left = face_locations[0]
        face_image = frame[top:bottom, left:right]
        cam.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        image2_face_encoding=face_recognition.face_encodings(face_image)[0]
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
