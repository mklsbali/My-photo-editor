from PIL import ImageFilter
from utils import cv_utils

# does not work: Filter, RankFilter


def contour(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.CONTOUR)
    return cv_utils.pil2cv_image(filtered)


def blur(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.BLUR)
    return cv_utils.pil2cv_image(filtered)


def max_filter(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.MaxFilter)
    return cv_utils.pil2cv_image(filtered)


def box_blur(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.BoxBlur)
    return cv_utils.pil2cv_image(filtered)


def usp_mask(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.UnsharpMask)
    return cv_utils.pil2cv_image(filtered)


def builtin_filter(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.BuiltinFilter)
    return cv_utils.pil2cv_image(filtered)


def c3d_lut(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.Color3DLUT)
    return cv_utils.pil2cv_image(filtered)


def detail(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.DETAIL)
    return cv_utils.pil2cv_image(filtered)


def edge_enhance(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.EDGE_ENHANCE)
    return cv_utils.pil2cv_image(filtered)


def edge_enhance_more(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return cv_utils.pil2cv_image(filtered)


def emboss(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.EMBOSS)
    return cv_utils.pil2cv_image(filtered)


def find_edges(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.FIND_EDGES)
    return cv_utils.pil2cv_image(filtered)


def gaussian_blur(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.GaussianBlur)
    return cv_utils.pil2cv_image(filtered)


def kernel(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.Kernel)
    return cv_utils.pil2cv_image(filtered)


def median(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.MedianFilter)
    return cv_utils.pil2cv_image(filtered)


def min_filter(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.MinFilter)
    return cv_utils.pil2cv_image(filtered)


def mode_filter(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.ModeFilter)
    return cv_utils.pil2cv_image(filtered)


def multi_band_filter(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.MultibandFilter)
    return cv_utils.pil2cv_image(filtered)


def sharpen(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.SHARPEN)
    return cv_utils.pil2cv_image(filtered)


def smooth(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.SMOOTH)
    return cv_utils.pil2cv_image(filtered)


def smooth_more(image):
    pil_im = cv_utils.cv2pil_image(image)
    filtered = pil_im.filter(ImageFilter.SMOOTH_MORE)
    return cv_utils.pil2cv_image(filtered)