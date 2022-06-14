import cv2 as cv
import numpy as np

import utils.cv_utils as cv_utils
import cv_filters_c


def red_image(image):
    return cv_utils.split_image(image)[2]


def green_image(image):
    return cv_utils.split_image(image)[1]


def blue_image(image):
    return cv_utils.split_image(image)[0]


def cython_filter(image, color):
    filtered = cv_filters_c.test_filter(image, color)
    return cv_utils.uint8_to_npy1(filtered)


def change_red_image(image, value):
    blue, green, red = cv_utils.split_image(image)
    red = cv.add(red, value)
    return cv.merge([blue, green, red])


def change_green_image(image, value):
    blue, green, red = cv_utils.split_image(image)
    green = cv.add(green, value)
    return cv.merge([blue, green, red])


def change_blue_image(image, value):
    blue, green, red = cv_utils.split_image(image)
    blue = cv.add(blue, value)
    return cv.merge([blue, green, red])
