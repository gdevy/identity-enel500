from pathlib import Path
from typing import List, Tuple

from cv2 import cv2


def download_model(destination: Path):
    import urllib.request

    haar_cascadess_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades" \
                         "/haarcascade_frontalface_default.xml "

    contents = urllib.request.urlopen(haar_cascadess_url).read()
    with open(destination, 'wb') as file:
        file.write(contents)


def validate_faces_bbox(faces: List) -> Tuple[bool, str]:
    if len(faces) > 1:
        return False, "Multiple faces detected"
    elif len(faces) < 1:
        return False, "Look at the camera and make sure your whole face is in the frame"

    return True, ""


def detect_faces(img) -> List:
    if not hasattr(detect_faces, 'model'):
        model_path = Path("haar_model.xml")
        download_model(model_path)
        detect_faces.model = cv2.CascadeClassifier(str(model_path))

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detect_faces.model.detectMultiScale(gray, 1.1, 4)

    return faces


def crop_face(face_bbox, img):
    x, y, h, w = face_bbox
    return img[x:x + w, y:y + h, :]
