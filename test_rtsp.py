import cv2

cap = cv2.VideoCapture("rtsp://student:s2024_645@10.2.94.200:554/cam/realmonitor?channel=1&subtype=0")

while True:
    _, image = cap.read()

    cv2.imshow("cap", image)
    cv2.waitKey(1)