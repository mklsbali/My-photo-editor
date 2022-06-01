import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QScrollBar, QListWidget, \
    QListWidgetItem, QHBoxLayout, QScrollArea, QVBoxLayout, QLineEdit
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


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'My photo editor'
        self.left = W_LEFT
        self.top = W_TOP
        self.width = W_WIDTH
        self.height = W_HEIGHT
        self.image_path = ''
        self.image_container = QLabel(self)
        self.image_label = QLabel(self.image_container)
        self.filter_container = QWidget(self)
        self.scroll_layout = None
        self.tmp_img = None
        self.resize_input = QLineEdit()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Image container
        self.image_container.setObjectName("image_container")
        self.image_container.resize(int(self.width*0.7), int(self.height*0.7))
        self.image_container.setStyleSheet(styles.image_container_style)
        self.image_container.move(int(self.width*0.25), 10)

        # Resize container
        resize_container = QWidget(self)
        resize_container.move(int(self.width*0.01), int(self.height*0.05))
        resize_container_layout = QHBoxLayout()
        resize_container.setLayout(resize_container_layout)
        resize_label = QLabel()
        resize_label.setText("%")
        resize_button = QPushButton("Resize")
        resize_button.clicked.connect(self.resize_img)
        # resize_button.move(int(self.width*0.1), int(self.height*0.1))
        resize_container_layout.addWidget(self.resize_input)
        resize_container_layout.addWidget(resize_label)
        resize_container_layout.addWidget(resize_button)

        # Select button
        select_button = QPushButton("Upload an image", self)
        select_button.clicked.connect(self.select_image)
        select_button.move(int(self.width*0.25), self.image_container.height()+15)

        # Save button
        select_button = QPushButton("Save image", self)
        select_button.clicked.connect(self.save_image)
        select_button.move(int(self.width*0.89), self.image_container.height()+15)

        # Filter container
        self.filter_container.setObjectName("filter_container")
        list_layout = QHBoxLayout(self.filter_container)
        self.filter_container.setLayout(list_layout)
        scroll = QScrollArea(self.filter_container)
        list_layout.addWidget(scroll)
        scroll_content = QWidget(scroll)
        self.scroll_layout = QHBoxLayout(scroll_content)
        scroll_content.setLayout(self.scroll_layout)

        self.filter_container.resize(int(self.width * 0.95), int(self.height * 0.21))
        self.filter_container.setStyleSheet(styles.filter_container_style)
        self.filter_container.move(int((self.width-self.filter_container.width())/2), self.image_container.height()+50)

        # Grayscale filter
        self.add_filter("Grayscale", styles.gs_button_style, self.set_grayscale_image)
        # Negative grayscale filter
        self.add_filter("Negative", styles.negative_button_style, self.set_negative_image)
        # Black and white filter
        self.add_filter("B & W", styles.b_w_button_style, self.set_b_w_image)
        # for i in range(50):
        #     self.add_filter("Negative", styles.negative_button_style, self.set_negative_image)

        scroll.setWidget(scroll_content)  # !!!1important
        # Image label
        self.set_image_label()
        self.show()

    def select_image(self):
        # Image select window
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_select_window = QFileDialog.getOpenFileName(self, 'OpenFile', '', "Image file (*.jpg *.png *.jpeg *.gif)", options=options)
        self.image_path = image_select_window[0]
        self.set_image_label()

    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        f_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if f_name:
            cv.imwrite(f_name, self.tmp_img)

    def set_image_label(self):
        pixmap = QPixmap(self.image_path)
        if pixmap.width() > self.image_container.width() or pixmap.height() > self.image_container.height():
            pixmap = pixmap.scaled(self.image_container.width()-130, self.image_container.height()-70, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.resize(pixmap.width(), pixmap.height())
        self.image_label.move(int((self.image_container.width()-self.image_label.width())/2), 10)

    def load_filtered_image(self, filtered):
        cv.imwrite(TMP_IMAGE_PATH, filtered)
        self.image_path = TMP_IMAGE_PATH
        self.set_image_label()

    def add_filter(self, filter_nane, style, function):
        one_filter = QVBoxLayout()
        one_filter_name = QLabel()
        one_filter_name.setText(filter_nane)
        one_filter_name.setAlignment(Qt.AlignCenter)
        one_filter.addWidget(one_filter_name)

        gs_button = QPushButton()
        gs_button.clicked.connect(function)
        gs_button.setStyleSheet(style)
        one_filter.addWidget(gs_button)
        self.scroll_layout.addLayout(one_filter)

    def resize_img(self):
        self.tmp_img = cv.imread(self.image_path)
        width = int(self.tmp_img.shape[1] * int(self.resize_input.text()) / 100)
        height = int(self.tmp_img.shape[0] * int(self.resize_input.text()) / 100)
        self.tmp_img = cv.resize(self.tmp_img, (width, height), interpolation=cv.INTER_AREA)
        self.load_filtered_image(self.tmp_img)

    def set_grayscale_image(self):
        self.tmp_img = cv.imread(self.image_path)
        gs_image = filters.gray_scale_image(self.tmp_img)
        self.load_filtered_image(gs_image)

    def set_negative_image(self):
        self.tmp_img = cv.imread(self.image_path)
        gs_image = filters.gray_scale_image(self.tmp_img)
        negative = filters.negative_image(gs_image)
        self.load_filtered_image(negative)

    def set_b_w_image(self):
        self.tmp_img = cv.imread(self.image_path)
        gs_image = filters.gray_scale_image(self.tmp_img)
        b_w = filters.b_w_image(gs_image)
        self.load_filtered_image(b_w)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
