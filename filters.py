import cv2 as cv


def gray_scale_image(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)


def negative_image(gs_image):
    return 255-gs_image


def b_w_image(gs_image):
    thresh, b_w_im = cv.threshold(gs_image, 127, 255, cv.THRESH_BINARY)
    return b_w_im
