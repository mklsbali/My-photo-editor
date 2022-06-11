import os.path
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QHBoxLayout, QScrollArea, \
    QVBoxLayout, QLineEdit, QColorDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from utils import cv_utils
import styles.styles as styles
import cv2 as cv
import filters.cv_filters
import filters.rgb2_x
import filters.bgr2_x
# import cv_filters_c

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
        self.rgb2x_functions = {
            'rgb2bgr': self.rgb2bgr,
            'rgb2bgr555': self.rgb2bgr555,
            'rgb2bgr565': self.rgb2bgr565,
            'rgb2bgra': self.rgb2bgra,
            'rgb2gray': self.rgb2gray,
            'rgb2hls': self.rgb2hls,
            'rgb2hls_full': self.rgb2hls_full,
            'rgb2hsv': self.rgb2hsv,
            'rgb2hsv_full': self.rgb2hsv_full,
            'rgb2lab': self.rgb2lab,
            'rgb2luv': self.rgb2luv,
            'rgb2lab1': self.rgb2lab1,
            'rgb2luv1': self.rgb2luv1,
            'rgb2rgba': self.rgb2rgba,
            'rgb2xyz': self.rgb2xyz,
            'rgb2ycr_cb': self.rgb2ycr_cb,
            'rgb2ycr_cb1': self.rgb2ycr_cb1,
            'rgb2ycr_yuv': self.rgb2ycr_yuv,
            'rgb2yuv_i420': self.rgb2yuv_i420,
            'rgb2yuv_iyuv': self.rgb2yuv_iyuv,
            'rgb2yv12': self.rgb2yv12,
        }

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
        # RGB2_X filters button
        rgb2x_filters_b = QPushButton("RGB2_X")
        rgb2x_filters_b.clicked.connect(self.reload_rgb2x_filters)
        # BGR2_X filters button
        bgr2x_filters_b = QPushButton("BGR2_X")
        bgr2x_filters_b.clicked.connect(self.reload_bgr2x_filters)
        filter_type_layout.addWidget(filter_type_text)
        filter_type_layout.addWidget(grayscale_filters_b)
        filter_type_layout.addWidget(rgb2x_filters_b)
        filter_type_layout.addWidget(bgr2x_filters_b)
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

    def reload_filters(self, function, message):
        print(message)
        self.load_cv_image(self.selected_image)
        self.tmp_image = self.selected_image
        self.remove_filters()
        function()

    def reload_grayscale_filters(self):
        self.reload_filters(self.load_grayscale_filters, "Reload grayscale filters")

    def reload_rgb2x_filters(self):
        self.reload_filters(self.load_rgb2_x_filters, "Reload rgb2x filters")

    def reload_bgr2x_filters(self):
        self.reload_filters(self.load_bgr2_x_filters, "Reload bgr2x filters")

    def setup_scroll_content(self):
        self.scroll_content = QWidget(self.scroll)
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)

    def load_grayscale_filters(self):
        self.setup_scroll_content()
        # Grayscale filter
        self.add_filter("Grayscale", self.set_grayscale_image)
        # Negative grayscale filter
        self.add_filter("Negative", self.set_negative_image)
        # # Black and white filter
        self.add_filter("B_W",  self.set_b_w_image)
        for i in range(50):
            self.add_filter("Negative", self.set_negative_image)

        self.scroll.setWidget(self.scroll_content)  # !!!important

    def load_rgb2_x_filters(self):
        self.setup_scroll_content()

        # for f in self.rgb2x_functions:
        #     print(f)
        #     self.add_filter(f[4:], self.rgb2x_functions[f])
        self.add_filter('rgb2bgr', self.rgb2bgr)
        # self.add_filter('rgb2bgr555', self.rgb2bgr555)
        # self.add_filter('rgb2bgr565', self.rgb2bgr565)
        # self.add_filter('rgb2bgra', self.rgb2bgra)
        self.add_filter('rgb2gray', self.rgb2gray)
        self.add_filter('rgb2hls', self.rgb2hls)
        self.add_filter('rgb2hls_full', self.rgb2hls_full)
        self.add_filter('rgb2hsv', self.rgb2hsv)
        self.add_filter('rgb2hsv_full', self.rgb2hsv_full)
        self.add_filter('rgb2lab', self.rgb2lab)
        self.add_filter('rgb2luv', self.rgb2luv)
        # self.add_filter('rgb2lab1', self.rgb2lab1)
        # self.add_filter('rgb2luv1', self.rgb2luv1)
        self.add_filter('rgb2rgba', self.rgb2rgba)
        self.add_filter('rgb2xyz', self.rgb2xyz)
        self.add_filter('rgb2ycr_cb', self.rgb2ycr_cb)
        # self.add_filter('rgb2ycr_cb1', self.rgb2ycr_cb1)
        self.add_filter('rgb2ycr_yuv', self.rgb2ycr_yuv)
        self.add_filter('rgb2yuv_i420', self.rgb2yuv_i420)
        # self.add_filter('rgb2yuv_iyuv', self.rgb2yuv_iyuv)
        # self.add_filter('rgb2yv12', self.rgb2yv12)


        self.scroll.setWidget(self.scroll_content)

    def load_bgr2_x_filters(self):
        self.setup_scroll_content()

        self.add_filter("bgr2hsv", self.bgr2hsv)
        self.add_filter("bgr2rgb", self.bgr2rgb)
        self.add_filter("bgr2lab", self.bgr2lab)

        self.scroll.setWidget(self.scroll_content)

    def load_color_filters(self):
        self.scroll_content = QWidget(self.scroll)
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        # Grayscale filter
        # self.add_filter("test_cf", self.test_cf)
        self.add_filter("hsv", self.set_hsv_image)
        self.add_filter("rgb", self.set_rgb_image)
        self.add_filter("lab", self.set_lab_image)
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
            self.color = color_class.na1me()
            print("Picked color: {}".format(self.color))
            self.cp_button.setStyleSheet(styles.cp_color(self.color))

    """filters functions
    """
    def set_image(self, filter_function_name, module,  was_clicked=True):
        """Generic function to call and apply a filter from another module"""
        filter_function = getattr(module, filter_function_name)
        if was_clicked:
            filtered = filter_function(self.selected_image)
            self.load_cv_image(filtered)
            self.tmp_image = filtered
        else:
            filtered = filter_function(cv.imread(GENERAL_FILTER_IMAGE_PATH))
        return filtered
    """grayscale"""
    def set_grayscale_image(self, was_clicked=True):
        return self.set_image("gray_scale_image", filters.cv_filters, was_clicked)

    def set_negative_image(self, was_clicked=True):
        return self.set_image("negative_image", filters.cv_filters, was_clicked)

    def set_b_w_image(self, was_clicked=True):
        return self.set_image("b_w_image", filters.cv_filters, was_clicked)
    """rgb2_x filters"""
    def rgb2bgr(self, was_clicked=True):
        return self.set_image("rgb2bgr", filters.rgb2_x, was_clicked)

    def rgb2bgr555(self, was_clicked=True):
        return self.set_image("rgb2bgr555", filters.rgb2_x, was_clicked)

    def rgb2bgr565(self, was_clicked=True):
        return self.set_image("rgb2bgr565", filters.rgb2_x, was_clicked)

    def rgb2bgra(self, was_clicked=True):
        return self.set_image("rgb2bgra", filters.rgb2_x, was_clicked)

    def rgb2gray(self, was_clicked=True):
        return self.set_image("rgb2gray", filters.rgb2_x, was_clicked)

    def rgb2hls(self, was_clicked=True):
        return self.set_image("rgb2hls", filters.rgb2_x, was_clicked)

    def rgb2hls_full(self, was_clicked=True):
        return self.set_image("rgb2hls_full", filters.rgb2_x, was_clicked)

    def rgb2hsv(self, was_clicked=True):
        return self.set_image("rgb2hsv", filters.rgb2_x, was_clicked)

    def rgb2hsv_full(self, was_clicked=True):
        return self.set_image("rgb2hsv_full", filters.rgb2_x, was_clicked)

    def rgb2lab(self, was_clicked=True):
        return self.set_image("rgb2lab", filters.rgb2_x, was_clicked)

    def rgb2luv(self, was_clicked=True):
        return self.set_image("rgb2luv", filters.rgb2_x, was_clicked)

    def rgb2lab1(self, was_clicked=True):
        return self.set_image("rgb2lab1", filters.rgb2_x, was_clicked)

    def rgb2luv1(self, was_clicked=True):
        return self.set_image("rgb2luv1", filters.rgb2_x, was_clicked)

    def rgb2rgba(self, was_clicked=True):
        return self.set_image("rgb2rgba", filters.rgb2_x, was_clicked)

    def rgb2xyz(self, was_clicked=True):
        return self.set_image("rgb2xyz", filters.rgb2_x, was_clicked)

    def rgb2ycr_cb(self, was_clicked=True):
        return self.set_image("rgb2ycr_cb", filters.rgb2_x, was_clicked)

    def rgb2ycr_cb1(self, was_clicked=True):
        return self.set_image("rgb2ycr_cb1", filters.rgb2_x, was_clicked)

    def rgb2ycr_yuv(self, was_clicked=True):
        return self.set_image("rgb2ycr_yuv", filters.rgb2_x, was_clicked)

    def rgb2yuv_i420(self, was_clicked=True):
        return self.set_image("rgb2yuv_i420", filters.rgb2_x, was_clicked)

    def rgb2yuv_iyuv(self, was_clicked=True):
        return self.set_image("rgb2yuv_iyuv", filters.rgb2_x, was_clicked)

    def rgb2yv12(self, was_clicked=True):
        return self.set_image("rgb2yv12", filters.rgb2_x, was_clicked)

    """bgr2_x"""
    def bgr2hsv(self, was_clicked=True):
        return self.set_image("bgr2hsv", filters.bgr2_x, was_clicked)

    def bgr2rgb(self, was_clicked=True):
        return self.set_image("bgr2rgb", filters.bgr2_x, was_clicked)

    def bgr2lab(self, was_clicked=True):
        return self.set_image("bgr2lab", filters.bgr2_x, was_clicked)

    # def test_cf(self, was_clicked=True):
    #     # if was_clicked:
    #     #     test_im = cv_filters.test_filter(self.selected_image, self.color)
    #     #     self.load_cv_image(test_im)
    #     #     self.tmp_image = test_im
    #     # else:
    #     #     test_im = cv_filters.test_filter(cv.imread(GENERAL_FILTER_IMAGE_PATH), self.color)
    #     # return test_im
    #     rgb = cv_utils.hex_to_rgb_color(self.color[1:])
    #     if was_clicked:
    #         filtered = cv_filters_c.test_filter(self.selected_image, rgb[0], rgb[1], rgb[2])
    #         # print(test_im)
    #         npy_im = cv_utils.uint8_to_npy1(filtered)
    #         self.load_cv_image(npy_im)
    #         # print(test_im)
    #         self.tmp_image = npy_im
    #     else:
    #         filtered = cv_filters_c.test_filter(cv.imread(GENERAL_FILTER_IMAGE_PATH), rgb[0], rgb[1], rgb[2])
    #         npy_im = cv_utils.uint8_to_npy1(filtered)
    #     return npy_im

    def apply_filter_image(self, f_name, function):
        f_path = os.path.join('styles', 'filter_images', f_name+'.png')
        if not os.path.exists(f_path):
            filter_image = function(was_clicked=False)
            resized_image = self.resize_img(img=filter_image, was_clicked=False)
            cv.imwrite(f_path, resized_image)
        return f_path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
