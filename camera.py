import cv2
import threading
from threading import Lock


class Camera:
    last_frame = None
    last_ready = None
    lock = Lock()
    capture = None
    result = False

    def __init__(self, rtsp_link):
        self.capture = cv2.VideoCapture(rtsp_link)
        thread = threading.Thread(target=self.rtsp_cam_buffer, args=(), name="rtsp_read_thread")
        thread.daemon = True
        thread.start()

    def rtsp_cam_buffer(self):
        while True:
            with self.lock:
                success = self.capture.grab()
                if not success:
                    continue  # Если не удалось получить кадр, переходим к следующей итерации
                self.result, self.last_frame = self.capture.retrieve()

    def getFrame(self):
        if self.last_frame is not None and self.result:  # Check if last frame is not None
            return self.last_frame.copy()
        else:
            return None
