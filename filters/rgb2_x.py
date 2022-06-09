import cv2 as cv


def rgb2hsv(image):
    return cv.cvtColor(image, cv.COLOR_RGB2HSV)


def rgb2bgr(image):
    return cv.cvtColor(image, cv.COLOR_RGB2BGR)


def rgb2lab(image):
    return cv.cvtColor(image, cv.COLOR_RGB2LAB)
