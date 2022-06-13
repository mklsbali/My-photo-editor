import cv2 as cv
from PyQt5 import QtGui, Qt
from PyQt5.QtGui import QPixmap
import ctypes as c
import numpy as np


def convert_cv_qt_pixmap(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)

    height, width, ch = rgb_image.shape
    bytes_per_line = ch * width
    q_image = QtGui.QImage(rgb_image.data, width, width, bytes_per_line, QtGui.QImage.Format_RGB888)
    return QPixmap.fromImage(q_image)


def hex_to_rgb_color(hex_color):
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def uint8_to_npy(src, height, width):
    ptr = c.cast(src, c.POINTER(c.c_uint8))
    array = np.ctypeslib.as_array(ptr, shape=(height, width, 3))
    return array


def uint8_to_npy1(src):
    return np.asarray(src, dtype=np.ubyte)


def split_image(image):
    return cv.split(image)


def merge_image(r, g, b):
    return cv.merge([r, g, b])
