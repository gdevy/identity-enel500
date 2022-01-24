# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import  copy, cv2

def acquirePhoto():
    instruction = "Look at the camera and make sure your whole face is in the frame"
    cam = cv2.VideoCapture(0)
    captured = False
    while captured == False:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        #    ----------
        frame1 = copy.deepcopy(frame)
        cv2.putText(frame1, instruction, (7, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.imshow("temp", frame1)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break
        #    -----------
        cv2.imwrite("temp.jpg", frame)
        # Load the cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Read the input image
        img = cv2.imread('temp.jpg')
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        faceCount = (len(faces))
        if faceCount>1:
            instruction = "Multiple faces detected"
            continue
        elif faceCount<1:
            instruction = "Look at the camera and make sure your whole face is in the frame"
            continue
       
        for (x, y, w, h) in faces:
            captured = True
            
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Display the output
        cv2.imshow('img', img)
        cv2.waitKey()
        cv2.imwrite('user.jpg', frame)
    cam.release()
    cv2.destroyAllWindows()


def preprocessPhoto():
    pass

def convertToTemplate():
    pass

def storeTemplate():
    pass


def aquireStoredTemplate():
    pass


def distanceCalculation():
    pass


acquirePhoto()