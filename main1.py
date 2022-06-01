import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QScrollBar, QListWidget, \
    QListWidgetItem, QHBoxLayout, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import styles
import cv2 as cv
import filters

W_LEFT = 100
W_TOP = 100
W_WIDTH = 1366
W_HEIGHT = 768
TMP_IMAGE_PATH = './images/tmp.png'


def set_image_label(image_path, image_container, image_label):
    pixmap = QPixmap(image_path)
    if pixmap.width() > image_container.width() or pixmap.height() > image_container.height():
        pixmap = pixmap.scaled(image_container.width() - 130, image_container.height() - 70,
                               Qt.KeepAspectRatio)
    
    image_label.setPixmap(pixmap)
    image_label.resize(pixmap.width(), pixmap.height())
    image_label.move(int((image_container.width() - image_label.width()) / 2), 10)
    
    
def select_image(container, image_label):
    # Image select window
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    image_select_window = QFileDialog.getOpenFileName(container, 'OpenFile', '', "Image file (*.jpg *.png *.jpeg *.gif)",
                                                      options=options)
    image_path = image_select_window[0]
    set_image_label(image_path, container, image_label)
    
    
def init_image_container(parent_container):
    image_container = QLabel(parent_container)
    image_container.setObjectName("image_container")
    image_container.resize(int(parent_container.width() * 0.7), int(parent_container.height() * 0.7))
    image_container.setStyleSheet(styles.image_container_style)
    image_container.move(int(parent_container.width() * 0.25), 10)
    return image_container
    
    
def init_ui():
    main_window = QWidget()
    main_window.setGeometry(W_LEFT, W_TOP, W_WIDTH, W_HEIGHT)
    
    image_container = init_image_container(main_window)
    image_label = QLabel(image_container)
    # Select button
    select_button = QPushButton("Upload an image", main_window)
    select_button.clicked.connect(select_image, (image_container, image_label))
    select_button.move(int(main_window.width() * 0.25), image_container.height() + 15)
    
    main_window.setWindowTitle("My image editor")
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_ui()
    sys.exit(app.exec_())
