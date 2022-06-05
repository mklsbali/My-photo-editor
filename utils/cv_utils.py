import cv2 as cv
from PyQt5 import QtGui, Qt
from PyQt5.QtGui import QPixmap


def convert_cv_qt_pixmap(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
    height, width, ch = rgb_image.shape
    bytes_per_line = ch * width
    q_image = QtGui.QImage(rgb_image.data, width, width, bytes_per_line, QtGui.QImage.Format_RGB888)
    return QPixmap.fromImage(q_image)
