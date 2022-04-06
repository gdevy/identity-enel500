"""
Functions handling face detection
"""
from pathlib import Path
from typing import List, Tuple

from cv2 import cv2


def download_model(destination: Path):
    """Downloads face detection model to specified path"""
    import urllib.request

    haar_cascadess_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades" \
                         "/haarcascade_frontalface_default.xml"

    contents = urllib.request.urlopen(haar_cascadess_url).read()
    with open(destination, 'wb') as file:
        file.write(contents)


def validate_faces_bbox(faces: List) -> Tuple[bool, str]:
    """
    Check the bounding boxes. Check that there is exactly one face and if not return an error.
    If not validated, also returns an error message
    :param faces: list of bounding box images
    :return: a tuple of validation result and error message
    """
    if len(faces) > 1:
        return False, "Multiple faces detected"
    elif len(faces) < 1:
        return False, "Look at the camera and make sure your whole face is in the frame"

    return True, ""


def detect_faces(img, *, min_width=200, min_height=200) -> List:
    """
    Apply face detection algorithm
    :param img: image as an array
    :return: list of face bounding boxes
    """

    if not hasattr(detect_faces, 'model'):
        model_path = Path("haar_model.xml")
        download_model(model_path)
        detect_faces.model = cv2.CascadeClassifier(str(model_path))

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    detected_bboxes = detect_faces.model.detectMultiScale(gray, 1.1, 4)
    faces = []
    for bbox in detected_bboxes:
        _, _, w, h = bbox
        if w > min_width and h > min_height:
            faces.append(bbox)

    return faces


def crop_face(face_bbox, img):
    """
    Crop an image according to a bounding box
    :param face_bbox: a tuple in the form of (x coord, y coord, x offset, y offset)
    :param img: image in array form
    :return: cropped image array
    """
    x, y, h, w = face_bbox
    return img[x:x + w, y:y + h, :]


def label_faces(face_bbox, img, min_size: Tuple = (200, 200)):
    min_h, min_w = min_size
    x, y, w, h = face_bbox
    if h > min_h and w > min_w:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return img
