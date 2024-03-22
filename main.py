import dlib
import numpy as np

from camera import Camera
import cv2
from datetime import datetime
import settings
from settings import cutting_accuracy
import threading
from process_face import process_face

cam = Camera("rtsp://student:s2024_645@10.2.94.200:554/cam/realmonitor?channel=1&subtype=0")

while True:
    image = cam.getFrame()  # Get the latest frame

    if image is not None:  # Check if the frame is valid

        x = 1200  # количество пикселей, которые нужно обрезать слева
        y = 400  # количество пикселей, которые нужно обрезать сверху
        width = image.shape[1] - x
        height = image.shape[0] - y

        # Обрезка изображения
        # image = cv2.resize(image, [1920, 1080])
        image = image[y:y + height, x:x + width]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = settings.face_detector(gray)

        for i, face in enumerate(faces):
            x1, y1, x2, y2 = face.left() - cutting_accuracy, face.top() - cutting_accuracy, \
                             face.right() + cutting_accuracy, face.bottom() + cutting_accuracy


            landmarks = settings.shape_predictor(gray, face)
            face_descriptor = settings.face_recognizer.compute_face_descriptor(image, landmarks)

            print(f"Дескриптор лица {i + 1}: {face_descriptor}")

            # thread = threading.Thread(target=process_face, args=(image, x1, y1, x2, y2))
            # thread.start()

        cv2.putText(image, datetime.now().strftime('%H:%M:%S'), (image.shape[0], 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)

        cv2.imshow("rtsp", image)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
