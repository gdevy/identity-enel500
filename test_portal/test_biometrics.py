from pathlib import Path

import pytest

from src.portal.biometrics.template import create_template, BiometricsError, pipeline, compare


def test_apply_template(sample_images):
    template = create_template(str(sample_images / "face1.jpg"))
    assert template.shape == (128,)

    assert not all(t == 0 for t in template)


def test_pipeline_success(sample_images):
    cat_path = sample_images / "face1.jpg"

    template = pipeline(cat_path)

    assert template.shape == (128,)


def test_pipeline_no_face(sample_images):
    cat_path = sample_images / "cat.jpeg"

    with pytest.raises(BiometricsError):
        pipeline(cat_path)


def test_compare_with_copy(sample_images):
    face_path = sample_images / "face1.jpg"

    template = pipeline(face_path)

    dist, auth = compare(template, face_path)

    assert auth
    assert dist == 0.0


def test_compare_with_self(sample_images):
    face_path = sample_images / "face1.jpg"
    face2_path = sample_images / "face2.jpg"

    template = pipeline(face_path)

    dist, auth = compare(template, face2_path)

    assert auth
    assert dist < 0.5


def test_compare_with_cat(sample_images):
    face_path = sample_images / "face1.jpg"
    cat_path = sample_images / "cat.jpeg"

    template = pipeline(face_path)

    dist, auth = compare(template, cat_path)

    assert not auth
    assert dist > 10.0
