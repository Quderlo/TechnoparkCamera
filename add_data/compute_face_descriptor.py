import cv2
import numpy as np

import settings


def compute_face_descriptor(image):
    # Конвертирование изображения в черно-белое для улучшения производительности детектора лиц
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Детекция лиц на изображении
    face_rects = settings.face_detector(gray)

    if len(face_rects) == 0:
        print("Лицо не обнаружено.")
        return None

    # Предполагается, что на изображении только одно лицо, если нужно обработать множество лиц, добавьте цикл по всем обнаруженным лицам
    face = face_rects[0]

    # Вычисление ключевых точек лица
    landmarks = settings.shape_predictor(gray, face)

    # Вычисление дескриптора лица
    face_descriptor = settings.face_recognizer.compute_face_descriptor(image, landmarks)

    return np.array(face_descriptor)
