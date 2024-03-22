import cv2
from datetime import datetime

import numpy as np

import settings
import dlib


def process_face(image, x1, y1, x2, y2):

    landmarks = settings.shape_predictor(image, dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2))

    cv2.imshow(datetime.now().strftime('%H:%M:%S'),
               cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2))

    print(np.array(settings.face_recognizer.compute_face_descriptor(image, landmarks, dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2))))
    return
