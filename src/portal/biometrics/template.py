"""
Functions handling creation of template
"""

from pathlib import Path
from typing import Tuple
import copy

import numpy as np

from deepface import DeepFace
from cv2 import cv2

from src.portal.biometrics.face_detection import detect_faces, label_faces, validate_faces_bbox

model_selection = "OpenFace"


def create_template(face_img) -> np.array:
    return np.array(DeepFace.represent(face_img, model_name=model_selection))


class BiometricsError(Exception):
    pass


def pipeline(image_path: Path) -> np.array:
    image = cv2.imread(str(image_path))

    faces = detect_faces(image)

    validated, msg = validate_faces_bbox(faces)
    if not validated:
        raise BiometricsError(msg)

    img = copy.deepcopy(image)
    for face in faces:
        img = label_faces(face, img)
    cv2.imwrite("temp.png", img)
    try:
        template = create_template(image)
    except ValueError:
        raise BiometricsError(f"Couldn't find face in {image_path} using the DeepFace algorithm")

    return template


def compare(template: np.array, probe_path: Path, threshold=1.0) -> Tuple[float, bool]:
    try:
        probe = pipeline(probe_path)
    except BiometricsError:
        print("Error creating template for probe. Auth failed")
        return float("inf"), False

    dist = np.linalg.norm(template - probe)

    return dist, dist < threshold
