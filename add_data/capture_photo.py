import cv2


def capture_photo():
    # Открываем подключение к камере (обычно 0 - это встроенная камера)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Не удалось открыть камеру.")
        return

    # Захватываем кадр с камеры
    ret, image = cap.read()

    if not ret:
        print("Не удалось захватить кадр.")
        return

    return image
