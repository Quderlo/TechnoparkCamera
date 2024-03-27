import asyncio
import os
import tempfile

from camera import Camera
import cv2
from datetime import datetime
import settings
from telegram_bot import Telegram_bot


async def send_data(image, descriptor):
    result, message, photo = telegram_bot.check_data(descriptor)
    if result is not None:
        await telegram_bot.send_data(image, photo, message)


async def main():
    if settings.rtsp:
        cam = Camera("rtsp://student:s2024_645@10.2.94.200:554/cam/realmonitor?channel=1&subtype=0")
    else:
        cam = Camera(0)
    cv2.waitKey(2000)

    while True:
        image = cam.getFrame()  # Get the latest frame

        if image is not None:  # Check if the frame is valid

            if settings.rtsp:
                x = 1200  # количество пикселей, которые нужно обрезать слева
                y = 400  # количество пикселей, которые нужно обрезать сверху
                width = image.shape[1] - x
                height = image.shape[0] - y
                image = image[y:y + height, x:x + width]

            try:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            except cv2.error as cv2e:
                print(f"cv2 error in gray. {cv2e}")
                continue

            faces = settings.face_detector(gray)

            for i, face in enumerate(faces):
                landmarks = settings.shape_predictor(gray, face)
                face_descriptor = settings.face_recognizer.compute_face_descriptor(image, landmarks)

                # Запускаем асинхронную функцию для отправки данных в Telegram
                await send_data(image, face_descriptor)

            if settings.rtsp:
                cv2.putText(image, datetime.now().strftime('%H:%M:%S'), (image.shape[0], 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)
            else:
                cv2.putText(image, datetime.now().strftime('%H:%M:%S'), (100, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)

            cv2.imshow("rtsp", image)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    telegram_bot = Telegram_bot()
    asyncio.run(main())
