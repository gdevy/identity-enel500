"""
Functions handling creation of template
"""

from pathlib import Path
from typing import List, Tuple
from deepface import DeepFace
from cv2 import cv2
import copy
import numpy as np

from src.portal.biometrics.face_detection import detect_faces, crop_face

model_selection = "OpenFace"


def create_template(face_img) -> np.array:
    return np.array(DeepFace.represent(face_img, model_name=model_selection))


def pipeline(image_path: Path) -> np.array:
    image = cv2.imread(str(image_path))

    faces = detect_faces(image)
    print(faces)
    if len(faces)==0:
        print(f"Couldn't find face in {image_path}")
        return []
    # cropped = crop_face(faces[0], image)
    img = copy.deepcopy(image)
    for face in faces:
        x, y, w, h = face
        if (h>200 and w>200):
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imwrite("temp.png", img)
    try:
        template = create_template(image)
    except ValueError as err:
        print(f"Couldn't find face in {image_path}")
        print(str(err))
        return []
    return template


def compare(template: np.array, probe_path: Path, threshold=1.0) -> Tuple[float, bool]:
    probe = pipeline(probe_path)
    print(template)
    print(probe)
    print(type(template[0]))
    print(type(probe[0]))
    dist = np.linalg.norm(template - probe)

    return dist, dist < threshold
