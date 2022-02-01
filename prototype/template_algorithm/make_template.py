from pathlib import Path
import numpy as np

from cv2 import cv2
from deepface import DeepFace

model_selection = "OpenFace"

p = Path("/Users/gregdevyatov/School/ENGG500/lfw/")

counts = dict()
for i, folder in enumerate(p.iterdir()):
    if folder.is_dir():
        counts[folder.name] = len(list(folder.iterdir()))

in_class_name = "Andy_Roddick"
in_class_embeddings = []
for image_p in (p / in_class_name).iterdir():
    image = cv2.imread(str(image_p))
    try:
        embedding = DeepFace.represent(image, model_name=model_selection)
    except ValueError as err:
        print(f"coulnd't find face in {image_p}")
        continue
    in_class_embeddings.append(np.array(embedding))

embeddings = np.array(in_class_embeddings)
inclass_mean = np.mean(embeddings, 0)

for person in list(p.iterdir())[:30]:
    dists = []
    for image_p in person.iterdir():
        image = cv2.imread(str(image_p))
        try:
            embedding = np.array(DeepFace.represent(image, model_name=model_selection))
        except ValueError as err:
            print(f"coulnd't find face in {image_p}")
            continue

        d = np.linalg.norm(embedding - inclass_mean)
        dists.append(d)

    print(dists)
