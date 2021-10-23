import time
import cv2
import face_recognition
import copy

# from PIL import Image
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
    #    ----------
    frame1 = copy.deepcopy(frame)
    cv2.putText(frame1, name, (7, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    cv2.imshow("temp", frame1)
    k = cv2.waitKey(1)
    if k % 256 == 27:
        print("Escape hit, closing...")
        a = 1
        break
#    -----------

if a == 0:
    while i < 11 and a == 0:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        #    ----------
        frame1 = copy.deepcopy(frame)
        cv2.putText(frame1, name, (7, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.imshow("temp", frame1)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break
        #    -----------
        cv2.imwrite("temp.jpg", frame)
        test_image = face_recognition.load_image_file('temp.jpg')
        face_locations = face_recognition.face_locations(test_image)
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = frame[top:bottom, left:right]
            cv2.imwrite(str(i) + '.jpg', face_image)
            # pil_image = Image.fromarray(face_image)
            # pil_image.save(str(i)+'.jpg')
            i = i + 1
cam.release()
cv2.destroyAllWindows()
