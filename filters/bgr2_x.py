import cv2 as cv


def bgr2hsv(image):
    return cv.cvtColor(image, cv.COLOR_RGB2HSV)


def bgr2rgb(image):
    return cv.cvtColor(image, cv.COLOR_BGR2RGB)


def bgr2lab(image):
    return cv.cvtColor(image, cv.COLOR_BGR2LAB)
