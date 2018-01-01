# import necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

def scan_faces():
    # init camera and grab a ref to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.hflip = True
    camera.vflip = True
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # allow camera to warm up
    time.sleep(0.1)

    # capture an image
    camera.capture(rawCapture, format='bgr')
    # At this point the image is available as stream.array
    img = rawCapture.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # import XML Classifiers
    face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.4.0/data/haarcascades/haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        return (1)
    else:
        return (0)
