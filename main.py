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
        self.main_label1 = QLabel(self)  # image_container, upload and save buttons
        self.main_label2 = QLabel(self)  # filters
        self.main_label3 = QLabel(self)  # options, resize
        self.image_container = QLabel(self.main_label1)
        self.image_label = QLabel(self.image_container)
        self.filter_container = QWidget(self.main_label2)
        self.scroll_layout = None
        self.tmp_img = None
        self.resize_input = QLineEdit()
        self.init_ui()

    def init_ui(self):
        # Init main window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Init main_label1
        self.init_main_label1()

        # Init main_label2
        self.init_main_label2()

        # Init main_label3
        self.init_main_label3()
        # Image label
        self.show()

    def init_main_label1(self):
        """Image"""
        # Init main_label1
        self.main_label1.resize(int(self.width * 0.75), int(self.height * 0.75))
        self.main_label1.move(int(self.width * 0.24), int(self.height * 0.02))
        # Image container
        self.image_container.setObjectName("image_container")
        self.image_container.resize(self.main_label1.width(), int(self.main_label1.height() * 0.9))
        self.image_container.setStyleSheet(styles.image_container_style)
        # self.image_container.move(int(self.width*0.25), 10)

        # Select button
        select_button = QPushButton("Upload an image", self.main_label1)
        select_button.clicked.connect(self.select_image)
        select_button.move(0, self.image_container.height() + 5)

        # Save button
        save_button = QPushButton("Save image", self.main_label1)
        save_button.clicked.connect(self.save_image)
        save_button.move(self.image_container.width() - save_button.width(), self.image_container.height() + 5)

    def init_main_label2(self):
        """Filters"""
        self.main_label2.setObjectName("main_label2")
        self.main_label2.resize(int(self.width * 0.98), int(self.height * 0.25))
        self.main_label2.move(int((self.width - self.main_label2.width()) / 2), self.image_container.height() + 50)
        self.main_label2.setStyleSheet(styles.main_label2_style)

        # Filter type
        filter_type = QWidget(self.main_label2)
        filter_type_layout = QHBoxLayout(filter_type)
        filter_type.setLayout(filter_type_layout)
        # Text
        filter_type_text = QLabel()
        filter_type_text.setText("Filter type")
        # Grayscale filters button
        grayscale_filters_b = QPushButton("Grayscale")
        grayscale_filters_b.clicked.connect(self.load_grayscale_filters)
        # Colorful filters button
        colorful_filters_b = QPushButton("Colorful")
        colorful_filters_b.clicked.connect(self.load_color_filters)
        filter_type_layout.addWidget(filter_type_text)
        filter_type_layout.addWidget(grayscale_filters_b)
        filter_type_layout.addWidget(colorful_filters_b)

        self.load_grayscale_filters()

    def init_main_label3(self):
        """Options"""
        self.main_label3.setObjectName("main_label3")
        self.main_label3.resize(int(self.width * 0.22), int(self.height * 0.70))
        self.main_label3.move(int(self.width*0.01), int(self.height*0.02))
        # self.main_label3.setStyleSheet(styles.main_label3_style)

        # Resize container
        resize_container = QWidget(self.main_label3)
        resize_container.move(10, 10)
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

    def load_grayscale_filters(self):
        # Filter container
        self.filter_container.setObjectName("filter_container")
        self.filter_container.resize(int(self.main_label2.width()), int(self.main_label2.height() * 0.85))
        self.filter_container.move(0, 30)
        h_list_layout = QHBoxLayout(self.filter_container)
        self.filter_container.setLayout(h_list_layout)
        scroll = QScrollArea(self.filter_container)
        h_list_layout.addWidget(scroll)
        scroll_content = QWidget(scroll)
        self.scroll_layout = QHBoxLayout(scroll_content)
        scroll_content.setLayout(self.scroll_layout)

        # Grayscale filter
        self.add_filter("Grayscale", styles.gs_button_style, self.set_grayscale_image)
        # Negative grayscale filter
        self.add_filter("Negative", styles.negative_button_style, self.set_negative_image)
        # Black and white filter
        self.add_filter("B & W", styles.b_w_button_style, self.set_b_w_image)
        for i in range(50):
            self.add_filter("Negative", styles.negative_button_style, self.set_negative_image)

        scroll.setWidget(scroll_content)  # !!!important

    def load_color_filters(self):
        # Filter container
        self.filter_container.setObjectName("filter_container")
        self.filter_container.resize(int(self.main_label2.width()), int(self.main_label2.height() * 0.85))
        self.filter_container.move(0, 30)
        h_list_layout = QHBoxLayout(self.filter_container)
        self.filter_container.setLayout(h_list_layout)
        scroll = QScrollArea(self.filter_container)
        h_list_layout.addWidget(scroll)
        scroll_content = QWidget(scroll)
        self.scroll_layout = QHBoxLayout(scroll_content)
        scroll_content.setLayout(self.scroll_layout)

        # Grayscale filter
        self.add_filter("Grayscale", styles.gs_button_style, self.set_grayscale_image)
        # Negative grayscale filter
        self.add_filter("Negative", styles.negative_button_style, self.set_negative_image)
        # Black and white filter
        self.add_filter("B & W", styles.b_w_button_style, self.set_b_w_image)
        for i in range(50):
            self.add_filter("B & W", styles.b_w_button_style, self.set_b_w_image)

        scroll.setWidget(scroll_content)  # !!!important

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
