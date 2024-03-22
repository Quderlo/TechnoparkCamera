from imutils import face_utils
import dlib
import cv2

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

cap = cv2.VideoCapture(0)

while True:
    # load the input image and convert it to grayscale
    _, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cutting_accuracy = 10

    # detect faces in the grayscale image
    rects = detector(gray, 0)
    print(rects)
    cv2.imshow("Window_name", image)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        x1, y1, x2, y2 = rect.left() - cutting_accuracy, rect.top() - cutting_accuracy, \
                         rect.right() + cutting_accuracy, rect.bottom() + cutting_accuracy
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array

        cv2.imshow("Gray", gray)

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image

        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

    # show the output image with the face detections + facial landmarks
    cv2.imshow("Output", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()