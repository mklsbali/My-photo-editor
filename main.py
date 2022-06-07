import os.path
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QHBoxLayout, QScrollArea, \
    QVBoxLayout, QLineEdit, QColorDialog
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt

from utils import cv_utils
import styles.styles as styles
import cv2 as cv
import cv_filters
import cv_filters_c

W_LEFT = 100
W_TOP = 100
W_WIDTH = 1366
W_HEIGHT = 768
TMP_IMAGE_PATH = './tmp/'
TMP_IMAGE_NAME = 'tmp.png'
GENERAL_FILTER_IMAGE_PATH = './styles/filter_images/test_photo.png'

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.filter_widgets = {
            "filter_texts": [],
            "filter_buttons": [],
            "filter_layouts": []
        }
        self.cp_button = QPushButton()
        self.title = 'My photo editor'
        self.left = W_LEFT
        self.top = W_TOP
        self.width = W_WIDTH
        self.height = W_HEIGHT
        self.selected_image_path = 'tmp/test_photo.png'
        self.main_label1 = QLabel(self)  # image_container, upload and save buttons
        self.main_label2 = QLabel(self)  # filters
        self.main_label3 = QLabel(self)  # options, resize
        # image container
        self.image_container = QLabel(self.main_label1)
        self.image_label = QLabel(self.image_container)
        # filter container
        self.image_container = QLabel(self.main_label1)
        self.image_label = QLabel(self.image_container)
        self.filter_container = QWidget()
        self.h_list_layout = QHBoxLayout()
        self.scroll = QScrollArea()
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout()
        self.selected_image = cv.imread(self.selected_image_path)
        self.tmp_image = cv.imread(self.selected_image_path)
        self.resize_input = QLineEdit()

        self.color = "#FFAABB"
        self.cp_button = QPushButton()

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
        self.load_image_from_path()

    def init_main_label3(self):
        """Options"""
        self.main_label3.setObjectName("main_label3")
        self.main_label3.resize(int(self.width * 0.22), int(self.height * 0.70))
        self.main_label3.move(int(self.width*0.01), int(self.height*0.02))
        # self.main_label3.setStyleSheet(styles.main_label3_style)

        # Resize container
        self.resize_input.setStyleSheet(styles.resize_input_style)
        resize_container = QWidget(self.main_label3)
        resize_container.move(int(self.main_label1.width()*0.01), int(self.main_label1.height()*0.01))
        resize_container_layout = QHBoxLayout()
        resize_container.setLayout(resize_container_layout)
        resize_label = QLabel()
        resize_label.setText("%")
        resize_label.setStyleSheet(styles.general_label_text_style)
        resize_button = QPushButton("Resize")
        resize_button.clicked.connect(self.resize_img)
        # resize_button.move(int(self.width*0.1), int(self.height*0.1))
        resize_container_layout.addWidget(self.resize_input)
        resize_container_layout.addWidget(resize_label)
        resize_container_layout.addWidget(resize_button)

        # Color picker
        cp_container = QWidget(self.main_label3)
        cp_container.move(int(self.main_label1.width()*0.01), int(self.main_label1.height()*0.07))
        cp_layout = QHBoxLayout()
        cp_container.setLayout(cp_layout)
        cp_text = QLabel()
        cp_text.setText("Pick a color")
        cp_text.setStyleSheet(styles.general_label_text_style)
        self.cp_button.setObjectName("cp_button")
        self.cp_button.setStyleSheet(styles.cp_color())
        self.cp_button.clicked.connect(self.pick_a_color)
        cp_layout.addWidget(cp_text)
        cp_layout.addWidget(self.cp_button)

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
        grayscale_filters_b.clicked.connect(self.reload_grayscale_filters)
        # Colorful filters button
        colorful_filters_b = QPushButton("Colorful")
        colorful_filters_b.clicked.connect(self.reload_color_filters)
        filter_type_layout.addWidget(filter_type_text)
        filter_type_layout.addWidget(grayscale_filters_b)
        filter_type_layout.addWidget(colorful_filters_b)
        self.filter_container = QWidget(self.main_label2)
        self.filter_container.setObjectName("filter_container")
        self.filter_container.resize(int(self.main_label2.width()), int(self.main_label2.height() * 0.85))
        self.filter_container.move(0, 30)

        self.h_list_layout = QHBoxLayout(self.filter_container)
        self.filter_container.setLayout(self.h_list_layout)

        self.scroll = QScrollArea(self.filter_container)
        self.h_list_layout.addWidget(self.scroll)

        # self.load_grayscale_filters()

    def remove_filters(self):
        for f_text in reversed(self.filter_widgets['filter_texts']):
            f_text.hide()
            self.filter_widgets['filter_texts'].pop()
        for f_button in reversed(self.filter_widgets['filter_buttons']):
            f_button.hide()
            self.filter_widgets['filter_buttons'].pop()
        for f_layout in reversed(self.filter_widgets['filter_layouts']):
            self.scroll_layout.removeItem(f_layout)
            self.filter_widgets['filter_layouts'].pop()

    def reload_grayscale_filters(self):
        print('Reload grayscale filters')
        gs_image = cv_filters.gray_scale_image(self.selected_image)
        self.tmp_image = gs_image
        self.load_cv_image(gs_image)
        self.remove_filters()
        self.load_grayscale_filters()


    def reload_color_filters(self):
        print('Reload color filters')
        self.load_cv_image(self.selected_image)
        self.tmp_image = self.selected_image
        self.remove_filters()
        self.load_color_filters()

    def load_grayscale_filters(self):
        self.scroll_content = QWidget(self.scroll)
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        # Grayscale filter
        self.add_filter("Grayscale", self.set_grayscale_image)
        # Negative grayscale filter
        self.add_filter("Negative", self.set_negative_image)
        # # Black and white filter
        self.add_filter("B_W",  self.set_b_w_image)
        for i in range(50):
            self.add_filter("Negative", self.set_negative_image)

        self.scroll.setWidget(self.scroll_content)  # !!!important

    def load_color_filters(self):
        self.scroll_content = QWidget(self.scroll)
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        # Grayscale filter
        self.add_filter("test_cf", self.test_cf)

        # Negative grayscale filter

        self.scroll.setWidget(self.scroll_content)  # !!!important

    def select_image(self):
        # Image select window
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_select_window = QFileDialog.getOpenFileName(self, 'OpenFile', '', "Image file (*.jpg *.png *.jpeg *.gif)", options=options)
        self.selected_image_path = image_select_window[0]
        self.selected_image = cv.imread(self.selected_image_path)
        self.load_image_from_path()

    def save_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        f_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if f_name:
            cv.imwrite(f_name, self.tmp_image)

    def load_image_from_path(self):
        pixmap = QPixmap(self.selected_image_path)
        if pixmap.width() > self.image_container.width() or pixmap.height() > self.image_container.height():
            pixmap = pixmap.scaled(self.image_container.width()-130, self.image_container.height()-70, Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.resize(pixmap.width(), pixmap.height())
        self.image_label.move(int((self.image_container.width()-self.image_label.width())/2), 10)

    def load_cv_image(self, cv_image):
        pixmap = cv_utils.convert_cv_qt_pixmap(cv_image)
        if pixmap.width() > self.image_container.width() or pixmap.height() > self.image_container.height():
            pixmap = pixmap.scaled(self.image_container.width() - 130, self.image_container.height() - 70,
                                   Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.resize(pixmap.width(), pixmap.height())
        self.image_label.move(int((self.image_container.width() - self.image_label.width()) / 2), 10)

    def save_filtered_image(self, filtered):
        """Saves a filtered image and set image_path to the saved image path"""
        if not os.path.exists(TMP_IMAGE_PATH):
            os.mkdir(TMP_IMAGE_PATH)
        self.selected_image_path = os.path.join(TMP_IMAGE_PATH, TMP_IMAGE_NAME)
        cv.imwrite(self.selected_image_path, filtered)

    def add_filter(self, filter_name, function):
        one_filter = QVBoxLayout()
        filter_text = QLabel()
        filter_text.setText(filter_name)
        filter_text.setAlignment(Qt.AlignCenter)
        one_filter.addWidget(filter_text)

        filter_button = QPushButton()
        filter_button.clicked.connect(lambda: function(was_clicked=True))
        f_image_path = self.apply_filter_image(filter_name, function)
        filter_button.setStyleSheet(styles.filter_style(f_image_path))
        one_filter.addWidget(filter_button)
        self.filter_widgets['filter_layouts'].append(one_filter)
        self.filter_widgets['filter_texts'].append(filter_text)
        self.filter_widgets['filter_buttons'].append(filter_button)
        self.scroll_layout.addLayout(one_filter)

    """options functions"""
    def resize_img(self, img=None, was_clicked=True):
        if was_clicked:
            width = int(self.tmp_image.shape[1] * int(self.resize_input.text()) / 100)
            height = int(self.tmp_image.shape[0] * int(self.resize_input.text()) / 100)
            resized_img = cv.resize(self.tmp_image, (width, height), interpolation=cv.INTER_AREA)
            self.load_cv_image(resized_img)
        else:
            width = int(img.shape[1] * 20 / 100)
            height = int(img.shape[0] * 20 / 100)
            resized_img = cv.resize(img, (width, height), interpolation=cv.INTER_AREA)
        return resized_img

    def pick_a_color(self):
        color_class = QColorDialog.getColor()
        if color_class.isValid():
            self.color = color_class.name()
            print("Picked color: {}".format(self.color))
            self.cp_button.setStyleSheet(styles.cp_color(self.color))

    """filters functions"""
    def set_grayscale_image(self, was_clicked=True):
        if was_clicked:
            gs_image = cv_filters.gray_scale_image(self.selected_image)
            self.load_cv_image(gs_image)
            self.tmp_image = gs_image
            print('clicked')
        else:
            gs_image = cv_filters.gray_scale_image(cv.imread(GENERAL_FILTER_IMAGE_PATH))
        return gs_image

    def set_negative_image(self, was_clicked=True):
        if was_clicked:
            negative = cv_filters.negative_image(self.selected_image)
            self.load_cv_image(negative)
            self.tmp_image = negative
        else:
            negative = cv_filters.negative_image(cv.imread(GENERAL_FILTER_IMAGE_PATH))
        return negative

    def set_b_w_image(self, was_clicked=True):
        if was_clicked:
            b_w = cv_filters.b_w_image(self.selected_image)
            self.load_cv_image(b_w)
            self.tmp_image = b_w
        else:
            b_w = cv_filters.b_w_image(cv.imread(GENERAL_FILTER_IMAGE_PATH))
        return b_w

    def apply_filter_image(self, f_name, function):
        f_path = os.path.join('styles', 'filter_images', f_name+'.png')
        if not os.path.exists(f_path):
            filter_image = function(was_clicked=False)
            resized_image = self.resize_img(img=filter_image, was_clicked=False)
            cv.imwrite(f_path, resized_image)
        return f_path

    def test_cf(self, was_clicked=True):
        # if was_clicked:
        #     test_im = cv_filters.test_filter(self.selected_image, self.color)
        #     self.load_cv_image(test_im)
        #     self.tmp_image = test_im
        # else:
        #     test_im = cv_filters.test_filter(cv.imread(GENERAL_FILTER_IMAGE_PATH), self.color)
        # return test_im
        rgb = cv_utils.hex_to_rgb_color(self.color[1:])
        if was_clicked:
            test_im = cv_filters_c.test_filter(self.selected_image, rgb[0], rgb[1], rgb[2])
            self.load_cv_image(test_im)
            self.tmp_image = test_im
        else:
            test_im = cv_filters_c.test_filter(cv.imread(GENERAL_FILTER_IMAGE_PATH), self.color)
        return test_im


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
