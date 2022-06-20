import os.path
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QPushButton, QHBoxLayout, QScrollArea, \
    QVBoxLayout, QLineEdit, QColorDialog, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import utils
from utils import cv_utils
import styles.styles as styles
import cv2 as cv
import filters.grayscale_filters
import filters.color_filters as color_filters
import filters.pillow_filters
import filters.rgb2_x
import filters.bgr2_x
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
        self.rgb_image = cv.imread(self.selected_image_path)
        self.bgr_image = cv.imread(self.selected_image_path)
        self.color = "#FFAABB"
        self.cp_button = QPushButton()
        self.red_slider = QSlider(Qt.Horizontal)
        self.green_slider = QSlider(Qt.Horizontal)
        self.blue_slider = QSlider(Qt.Horizontal)
        self.red_slider_value = QLabel()
        self.green_slider_value = QLabel()
        self.blue_slider_value = QLabel()
        self.r_image = color_filters.red_image(self.selected_image)
        self.g_image = cv.imread(self.selected_image_path)
        self.b_image = cv.imread(self.selected_image_path)
        self.init_ui()
        self.r_s_values = [0]
        self.g_s_values = [0]
        self.b_s_values = [0]
        self.slider_history = []

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

        # Red slider
        self.add_slider(self.red_slider, self.red_slider_value, 0.01, 0.20, self.red_slider_change, "Red")
        self.add_slider(self.green_slider, self.green_slider_value, 0.01, 0.30, self.green_slider_change, "Green")
        self.add_slider(self.blue_slider, self.blue_slider_value, 0.01, 0.40, self.blue_slider_change, "Blue")

    def add_slider(self, s, s_value, pos_x, pos_y, function, text):
        r_slider_container = QWidget(self.main_label3)
        r_slider_container.move(int(self.main_label1.width()*pos_x), int(self.main_label1.height()*pos_y))
        slider_layout = QHBoxLayout()
        r_slider_container.setLayout(slider_layout)
        slider_text = QLabel()
        slider_text.setMinimumWidth(50)
        slider_text.setText(text)
        s.setMinimumWidth(170)
        s.setMinimum(0)
        s.setMaximum(255)
        s.setSingleStep(1)
        s_value.setText("       0")
        s.valueChanged.connect(function)
        slider_layout.addWidget(slider_text)
        slider_layout.addWidget(s)
        slider_layout.addWidget(s_value)

    def get_last_changed_image(self):
        if len(self.slider_history) == 0:
            return self.selected_image

        if self.slider_history[-1] == "red":
            src = self.r_image
        elif self.slider_history[-1] == "green":
            src = self.g_image
        else:
            src = self.b_image
        return src

    def red_slider_change(self):
        if self.red_slider.value() == 0 and self.green_slider.value() == 0 and self.blue_slider.value() == 0:
            self.tmp_image = self.selected_image
        self.r_s_values.append(self.red_slider.value())
        self.red_slider_value.setText("       "+str(self.red_slider.value()))
        self.tmp_image = color_filters.change_red_image(self.tmp_image, self.r_s_values[-1]-self.r_s_values[-2])
        self.load_cv_image(self.tmp_image)
        if self.red_slider.value() == 0 and self.green_slider.value() == 0 and self.blue_slider.value() == 0:
            self.load_cv_image(self.selected_image)

    def green_slider_change(self):
        if self.red_slider.value() == 0 and self.green_slider.value() == 0 and self.blue_slider.value() == 0:
            self.tmp_image = self.selected_image
        self.g_s_values.append(self.green_slider.value())
        self.green_slider_value.setText("       "+str(self.green_slider.value()))
        self.tmp_image = color_filters.change_green_image(self.tmp_image, self.g_s_values[-1]-self.g_s_values[-2])
        self.load_cv_image(self.tmp_image)

    def blue_slider_change(self):
        if self.red_slider.value() == 0 and self.green_slider.value() == 0 and self.blue_slider.value() == 0:
            self.tmp_image = self.selected_image
        self.b_s_values.append(self.blue_slider.value())
        self.blue_slider_value.setText("       "+str(self.blue_slider.value()))
        self.tmp_image = color_filters.change_blue_image(self.tmp_image, self.b_s_values[-1]-self.b_s_values[-2])
        self.load_cv_image(self.tmp_image)

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
        # Color filters
        color_filters_b = QPushButton("Color")
        color_filters_b.clicked.connect(self.reload_color_filters)
        # RGB2_X filters button
        rgb2x_filters_b = QPushButton("RGB2_X")
        rgb2x_filters_b.clicked.connect(self.reload_rgb2x_filters)
        # BGR2_X filters button
        bgr2x_filters_b = QPushButton("BGR2_X")
        bgr2x_filters_b.clicked.connect(self.reload_bgr2x_filters)
        # Pillow filters button
        pillow_b = QPushButton("Pillow")
        pillow_b.clicked.connect(self.reload_pillow_filter)

        filter_type_layout.addWidget(filter_type_text)
        filter_type_layout.addWidget(grayscale_filters_b)
        filter_type_layout.addWidget(color_filters_b)
        filter_type_layout.addWidget(rgb2x_filters_b)
        filter_type_layout.addWidget(bgr2x_filters_b)
        filter_type_layout.addWidget(pillow_b)
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

    def reload_color_filters(self):
        self.reload_filters(self.load_color_filters, "Reload color filters")

    def reload_rgb2x_filters(self):
        self.reload_filters(self.load_rgb2_x_filters, "Reload rgb2x filters")

    def reload_bgr2x_filters(self):
        self.reload_filters(self.load_bgr2_x_filters, "Reload bgr2x filters")

    def reload_pillow_filter(self):
        self.reload_filters(self.load_pillow_filters, "Reload pillow filters")

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
        self.scroll.setWidget(self.scroll_content)  # !!!important

    def load_color_filters(self):
        self.setup_scroll_content()

        # self.add_filter("test_cython", self.test_cython_filter)
        self.add_filter("red", self.red_image)
        self.add_filter("green", self.green_image)
        self.add_filter("blue", self.blue_image)

        self.scroll.setWidget(self.scroll_content)  # !!!important

    def load_rgb2_x_filters(self):
        self.setup_scroll_content()

        self.rgb_image = self.selected_image
        self.load_cv_image(self.rgb_image)

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
        # self.add_filter('lab1', self.rgb2lab1)
        # self.add_filter('luv1', self.rgb2luv1)
        # self.add_filter('rgb2rgba', self.rgb2rgba)
        self.add_filter('rgb2xyz', self.rgb2xyz)
        self.add_filter('rgb2ycr_cb', self.rgb2ycr_cb)
        # self.add_filter('ycr_cb1', self.rgb2ycr_cb1)
        self.add_filter('rgb2ycr_yuv', self.rgb2ycr_yuv)
        # self.add_filter('rgb2yuv_i420', self.rgb2yuv_i420)
        self.add_filter('rgb2yuv_iyuv', self.rgb2yuv_iyuv)
        # self.add_filter('rgb2yv12', self.rgb2yv12)

        self.scroll.setWidget(self.scroll_content)

    def load_bgr2_x_filters(self):
        self.setup_scroll_content()
        self.bgr_image = filters.rgb2_x.rgb2bgr(self.selected_image)
        self.load_cv_image(self.bgr_image)
        self.add_filter('bgr2rgb', self.bgr2rgb)
        # self.add_filter('bgr2bgr555', self.bgr2bgr555)
        # self.add_filter('bgr2bgr565', self.bgr2bgr565)
        # self.add_filter('bgr22bgra', self.bgr2bgra)
        self.add_filter('bgr2gray', self.bgr2gray)
        self.add_filter('bgr2hls', self.bgr2hls)
        self.add_filter('bgr2hls_full', self.bgr2hls_full)
        self.add_filter('bgr2hsv', self.bgr2hsv)
        self.add_filter('bgr2hsv_full', self.bgr2hsv_full)
        self.add_filter('bgr2lab', self.bgr2lab)
        self.add_filter('bgr2luv', self.bgr2luv)
        # self.add_filter('bgr2lab1', self.bgr2lab1)
        # self.add_filter('bgr2luv1', self.bgr2luv1)
        # self.add_filter('bgr2bgra', self.bgr2bgra)
        self.add_filter('bgr2xyz', self.bgr2xyz)
        self.add_filter('bgr2ycr_cb', self.bgr2ycr_cb)
        # self.add_filter('bgr2ycr_cb1', self.bgr2ycr_cb1)
        self.add_filter('bgr2ycr_yuv', self.bgr2ycr_yuv)
        # self.add_filter('bgr2yuv_i420', self.bgr2yuv_i420)
        self.add_filter('bgr2yuv_iyuv', self.bgr2yuv_iyuv)
        # self.add_filter('bgr2yv12', self.bgr2yv12)

        self.scroll.setWidget(self.scroll_content)

    def load_pillow_filters(self):
        self.setup_scroll_content()
        self.add_filter("Contour", self.contour)
        self.add_filter("Blur", self.blur)
        self.add_filter("Max", self.max_filter)
        self.add_filter("Min", self.min_filter)
        # self.add_filter("Box blur", self.box_blur)
        self.add_filter("Mask", self.usp_mask)
        # self.add_filter("Builtin", self.builtin_filter)
        # self.add_filter("3D lut", self.c3d_lut)
        self.add_filter("Detail", self.detail)
        self.add_filter("Enhance", self.edge_enhance)
        self.add_filter("Enhance_m", self.edge_enhance_more)
        self.add_filter("Edges", self.find_edges)
        self.add_filter("Gaussian", self.gaussian_blur)
        # self.add_filter("Kernel", self.kernel)
        self.add_filter("Median", self.median)
        self.add_filter("Mode", self.mode_filter)
        self.add_filter("Sharpen", self.sharpen)
        # self.add_filter("Multi", self.multi_band_filter)
        self.add_filter("Smooth", self.smooth)
        self.add_filter("Smooth m", self.smooth_more)
        self.scroll.setWidget(self.scroll_content)  # !!!important

    def select_image(self):
        # Image select window
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image_select_window = QFileDialog.getOpenFileName(self, 'OpenFile', '', "Image file (*.jpg *.png *.jpeg *.gif)", options=options)
        if image_select_window[0]:
            self.selected_image_path = image_select_window[0]
            self.selected_image = cv.imread(self.selected_image_path)
            self.rgb_image = self.selected_image
            self.tmp_image = self.selected_image
            self.bgr_image = filters.rgb2_x.rgb2bgr(self.rgb_image)
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

    """filters functions
    """
    def set_image(self, src_image, filter_function_name, module,  was_clicked=True):
        """Generic function to call and apply a filter from another module"""
        filter_function = getattr(module, filter_function_name)
        if was_clicked:
            filtered = filter_function(src_image)
            self.load_cv_image(filtered)
            self.tmp_image = filtered
        else:
            filtered = filter_function(src_image)
        return filtered

    def set_image_with_arguments(self, src_image, filter_function_name, module, args, was_clicked=True):
        filter_function = getattr(module, filter_function_name)
        if was_clicked:
            filtered = filter_function(src_image, args)
            self.load_cv_image(filtered)
            self.tmp_image = filtered
        else:
            filtered = filter_function(src_image, args)
        return filtered
    """other filters"""
    def set_grayscale_image(self, was_clicked=True):
        return self.set_image(self.rgb_image, "gray_scale_image", filters.grayscale_filters, was_clicked)

    def set_negative_image(self, was_clicked=True):
        return self.set_image(self.rgb_image, "negative_image", filters.grayscale_filters, was_clicked)

    def set_b_w_image(self, was_clicked=True):
        return self.set_image(self.rgb_image, "b_w_image", filters.grayscale_filters, was_clicked)
    """color filters"""
    def red_image(self, was_clicked=True):
        return self.set_image(self.rgb_image, "red_image", color_filters, was_clicked)

    def green_image(self, was_clicked=True):
        return self.set_image(self.rgb_image, "green_image", color_filters, was_clicked)

    def blue_image(self, was_clicked=True):
        return self.set_image(self.rgb_image, "blue_image", color_filters, was_clicked)
    """rgb2_x filters"""
    def rgb2bgr(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2bgr", filters.rgb2_x, was_clicked)

    def rgb2bgr555(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2bgr555", filters.rgb2_x, was_clicked)

    def rgb2bgr565(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2bgr565", filters.rgb2_x, was_clicked)

    def rgb2bgra(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2bgra", filters.rgb2_x, was_clicked)

    def rgb2gray(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2gray", filters.rgb2_x, was_clicked)

    def rgb2hls(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2hls", filters.rgb2_x, was_clicked)

    def rgb2hls_full(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2hls_full", filters.rgb2_x, was_clicked)

    def rgb2hsv(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2hsv", filters.rgb2_x, was_clicked)

    def rgb2hsv_full(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2hsv_full", filters.rgb2_x, was_clicked)

    def rgb2lab(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2lab", filters.rgb2_x, was_clicked)

    def rgb2luv(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2luv", filters.rgb2_x, was_clicked)

    def rgb2lab1(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2lab1", filters.rgb2_x, was_clicked)

    def rgb2luv1(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2luv1", filters.rgb2_x, was_clicked)

    def rgb2rgba(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2rgba", filters.rgb2_x, was_clicked)

    def rgb2xyz(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2xyz", filters.rgb2_x, was_clicked)

    def rgb2ycr_cb(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2ycr_cb", filters.rgb2_x, was_clicked)

    def rgb2ycr_cb1(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2ycr_cb1", filters.rgb2_x, was_clicked)

    def rgb2ycr_yuv(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2ycr_yuv", filters.rgb2_x, was_clicked)

    def rgb2yuv_i420(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2yuv_i420", filters.rgb2_x, was_clicked)

    def rgb2yuv_iyuv(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2yuv_iyuv", filters.rgb2_x, was_clicked)

    def rgb2yv12(self, was_clicked=True):
        return self.set_image(self.rgb_image, "rgb2yv12", filters.rgb2_x, was_clicked)

    """bgr2_x filters"""
    def bgr2rgb(self, was_clicked=True):
        return self.set_image(self.bgr_image, "bgr2rgb", filters.bgr2_x, was_clicked)

    def bgr2bgr555(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2bgr555", filters.bgr2_x, was_clicked)

    def bgr2bgr565(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2bgr565", filters.bgr2_x, was_clicked)

    def bgr2bgra(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2bgra", filters.bgr2_x, was_clicked)

    def bgr2gray(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2gray", filters.bgr2_x, was_clicked)

    def bgr2hls(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2hls", filters.bgr2_x, was_clicked)

    def bgr2hls_full(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2hls_full", filters.bgr2_x, was_clicked)

    def bgr2hsv(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2hsv", filters.bgr2_x, was_clicked)

    def bgr2hsv_full(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2hsv_full", filters.bgr2_x, was_clicked)

    def bgr2lab(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2lab", filters.bgr2_x, was_clicked)

    def bgr2luv(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2luv", filters.bgr2_x, was_clicked)

    def bgr2lab1(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2lab1", filters.bgr2_x, was_clicked)

    def bgr2luv1(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2luv1", filters.bgr2_x, was_clicked)

    def bgr2xyz(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2xyz", filters.bgr2_x, was_clicked)

    def bgr2ycr_cb(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2ycr_cb", filters.bgr2_x, was_clicked)

    def bgr2ycr_cb1(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2ycr_cb1", filters.bgr2_x, was_clicked)

    def bgr2ycr_yuv(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2ycr_yuv", filters.bgr2_x, was_clicked)

    def bgr2yuv_i420(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2yuv_i420", filters.bgr2_x, was_clicked)

    def bgr2yuv_iyuv(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2yuv_iyuv", filters.bgr2_x, was_clicked)

    def bgr2yv12(self, was_clicked=True):
        return self.set_image(self.rgb_image, "bgr2yv12", filters.bgr2_x, was_clicked)

    """PIL"""
    def contour(self, was_clicked=True):
        return self.set_image(self.rgb_image, "contour", filters.pillow_filters, was_clicked)

    def blur(self, was_clicked=True):
        return self.set_image(self.rgb_image, "blur", filters.pillow_filters, was_clicked)

    def min_filter(self, was_clicked=True):
        return self.set_image(self.rgb_image, "min_filter", filters.pillow_filters, was_clicked)

    def max_filter(self, was_clicked=True):
        return self.set_image(self.rgb_image, "max_filter", filters.pillow_filters, was_clicked)

    def box_blur(self, was_clicked=True):
        return self.set_image(self.rgb_image, "box_blur", filters.pillow_filters, was_clicked)

    def usp_mask(self, was_clicked=True):
        return self.set_image(self.rgb_image, "usp_mask", filters.pillow_filters, was_clicked)

    def builtin_filter(self, was_clicked=True):
        return self.set_image(self.rgb_image, "builtin_filter", filters.pillow_filters, was_clicked)

    def c3d_lut(self, was_clicked=True):
        return self.set_image(self.rgb_image, "c3d_lut", filters.pillow_filters, was_clicked)

    def detail(self, was_clicked=True):
        return self.set_image(self.rgb_image, "detail", filters.pillow_filters, was_clicked)

    def edge_enhance(self, was_clicked=True):
        return self.set_image(self.rgb_image, "edge_enhance", filters.pillow_filters, was_clicked)

    def edge_enhance_more(self, was_clicked=True):
        return self.set_image(self.rgb_image, "edge_enhance_more", filters.pillow_filters, was_clicked)

    def emboss(self, was_clicked=True):
        return self.set_image(self.rgb_image, "emboss", filters.pillow_filters, was_clicked)

    def find_edges(self, was_clicked=True):
        return self.set_image(self.rgb_image, "find_edges", filters.pillow_filters, was_clicked)

    def gaussian_blur(self, was_clicked=True):
        return self.set_image(self.rgb_image, "gaussian_blur", filters.pillow_filters, was_clicked)

    def kernel(self, was_clicked=True):
        return self.set_image(self.rgb_image, "kernel", filters.pillow_filters, was_clicked)

    def median(self, was_clicked=True):
        return self.set_image(self.rgb_image, "median", filters.pillow_filters, was_clicked)

    def mode_filter(self, was_clicked=True):
        return self.set_image(self.rgb_image, "mode_filter", filters.pillow_filters, was_clicked)

    def multi_band_filter(self, was_clicked=True):
        return self.set_image(self.rgb_image, "multi_band_filter", filters.pillow_filters, was_clicked)

    def sharpen(self, was_clicked=True):
        return self.set_image(self.rgb_image, "sharpen", filters.pillow_filters, was_clicked)

    def smooth(self, was_clicked=True):
        return self.set_image(self.rgb_image, "smooth", filters.pillow_filters, was_clicked)

    def smooth_more(self, was_clicked=True):
        return self.set_image(self.rgb_image, "smooth_more", filters.pillow_filters, was_clicked)


    """"""
    def test_cython_filter(self, was_clicked=True):
        rgb_color = cv_utils.hex_to_rgb_color(self.color[1:])
        return self.set_image_with_arguments(self.rgb_image, "cython_filter", color_filters, args=rgb_color, was_clicked=was_clicked)

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

