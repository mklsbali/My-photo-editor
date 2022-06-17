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


# def blur(image):
#     pil_im = cv_utils.cv2pil_image(image)
#     filtered = pil_im.filter(ImageFilter.BoxBlur)
#     return cv_utils.pil2cv_image(filtered)
#
#
# def blur(image):
#     pil_im = cv_utils.cv2pil_image(image)
#     filtered = pil_im.filter(ImageFilter.BLUR)
#     return cv_utils.pil2cv_image(filtered)
#
#
# def blur(image):
#     pil_im = cv_utils.cv2pil_image(image)
#     filtered = pil_im.filter(ImageFilter.BLUR)
#     return cv_utils.pil2cv_image(filtered)