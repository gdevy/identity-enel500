from pathlib import Path
from typing import List, Tuple

from cv2 import cv2

import numpy as np

from src.portal.biometrics.face_detection import detect_faces, crop_face

model_selection = "OpenFace"


def create_template(face_img) -> np.array:
    return np.array(DeepFace.represent(face_img, model_name=model_selection))


def pipeline(image_path: Path) -> np.array:
    image = cv2.imread(str(image_path))

    faces = detect_faces(image)

    cropped = crop_face(faces[0], image)

    try:
        template = create_template(cropped)
    except ValueError as err:
        print(f"Couldn't find face in {image_path}")
        return None
    return template


def compare(template: np.array, probe_path: Path, threshold=1.0) -> Tuple[float, bool]:

    probe = pipeline(probe_path)
    dist = np.linalg.norm(template - probe)

    return dist, dist < threshold
