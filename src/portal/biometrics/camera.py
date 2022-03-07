"""
Interfaces with the camera to create template
"""
import copy
from pathlib import Path

from cv2 import cv2

from src.portal.biometrics.face_detection import detect_faces, validate_faces_bbox


def create_probe(output_file: Path):
    cam = cv2.VideoCapture(0)

    retry_msg = ""
    while True:
        img = capture_photo(cam, retry_msg)

        faces = detect_faces(img)

        validated, msg = validate_faces_bbox(faces)

        if validated:
            retry_instructions = "Acquired probe. Press ESC to save and exit, press ENTER to take a new picture"

            x, y, h, w = faces[0]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, retry_instructions, (7, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            cv2.imshow('img', img)

            k = cv2.waitKey()
            if k == 13:
                retry_msg = ""
                continue
            elif k == 26:
                cv2.imwrite(str(output_file), img)
                break
            cv2.destroyWindow('img')
        else:
            retry_msg = msg

    cam.release()
    cv2.destroyAllWindows()


def capture_photo(cam, retry_msg=None):
    instruction = "Look at the camera and make sure your whole face is in the frame. Press ESC to quit, ENTER to " \
                  "capture "

    while True:
        ret, frame = cam.read()
        if not ret:
            raise RuntimeError("Failed to capture frame with camera")

        img = copy.deepcopy(frame)

        if retry_msg:
            instruction = retry_msg + "\n" + instruction
        cv2.putText(frame, instruction, (7, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 3)
        cv2.imshow("frame", frame)

        k = cv2.waitKey(10)
        if k == 26:
            return None

        elif k == 13:
            return img
