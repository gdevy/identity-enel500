from pathlib import Path

from cv2 import cv2
import face_recognition

p = Path("/Users/gregdevyatov/School/ENGG500/lfw/Aaron_Eckhart/Aaron_Eckhart_0001.jpg")

# load the input image and convert it from BGR (OpenCV ordering)
# to dlib ordering (RGB)
image = cv2.imread(str(p))
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

boxes = face_recognition.face_locations(rgb, model='cnn')
# compute the facial embedding for the face

encodings = face_recognition.face_encodings(rgb, boxes)
# loop over the encodings

for encoding in encodings:
    # add each encoding + name to our set of known names and
    # encodings
    knownEncodings.append(encoding)
    knownNames.append(name)
