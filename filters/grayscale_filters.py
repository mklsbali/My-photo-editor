import cv2 as cv
import numpy as np
import utils.cv_utils as cv_utils


def gray_scale_image(image):
    return cv.cvtColor(image, cv.COLOR_RGB2GRAY)


def negative_image(image):
    gs_image = gray_scale_image(image)
    return 255-gs_image


def b_w_image(image, threshold=127):
    gs_image = gray_scale_image(image)
    thresh, b_w_im = cv.threshold(gs_image, threshold, 255, cv.THRESH_BINARY)
    return b_w_im


def test_filter(image, hex_color):
    rgb_color = cv_utils.hex_to_rgb_color(hex_color[1:])
    print(type(image))
    width = image.shape[1]
    height = image.shape[0]
    for j in np.arange(0, height):
        for i in np.arange(0, width):
            image[j][i][0] = image[j][i][0] + rgb_color[0] // 2
            image[j][i][1] = image[j][i][1] + rgb_color[1] // 2
            image[j][i][2] = image[j][i][2] + rgb_color[2] // 2

    return image
