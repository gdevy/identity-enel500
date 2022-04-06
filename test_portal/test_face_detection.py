from cv2 import cv2

from src.portal.biometrics.face_detection import label_faces, validate_faces_bbox, detect_faces, crop_face


def test_detect_face(sample_images):
    face_path = sample_images / 'face1.jpg'
    face = cv2.imread(str(face_path))

    detected_faces = detect_faces(face)

    assert len(detected_faces) == 1


def test_detect_face_cat(sample_images):
    face_path = sample_images / 'cat.jpeg'
    face = cv2.imread(str(face_path))

    detected_faces = detect_faces(face)

    assert len(detected_faces) == 0


def test_label_faces(sample_images):
    face_path = sample_images / 'face1.jpg'
    face = cv2.imread(str(face_path))
    face_bbox = (10, 20, 220, 220)

    label_faces(face_bbox, face)


def test_crop_image(sample_images):
    face_path = sample_images / 'face1.jpg'
    face = cv2.imread(str(face_path))
    face_bbox = (10, 20, 220, 220)

    cropped_face = crop_face(face_bbox, face)

    assert cropped_face.shape == (220, 220, 3)
