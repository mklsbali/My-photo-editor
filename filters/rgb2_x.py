import cv2 as cv


def rgb2bgr(image):
    return cv.cvtColor(image, cv.COLOR_RGB2BGR)


def rgb2bgr555(image):
    return cv.cvtColor(image, cv.COLOR_RGB2BGR555)


def rgb2bgr565(image):
    return cv.cvtColor(image, cv.COLOR_RGB2BGR565)


def rgb2bgra(image):
    return cv.cvtColor(image, cv.COLOR_RGB2BGRA)


def rgb2gray(image):
    return cv.cvtColor(image, cv.COLOR_RGB2GRAY)


def rgb2hls(image):
    return cv.cvtColor(image, cv.COLOR_RGB2HLS)


def rgb2hls_full(image):
    return cv.cvtColor(image, cv.COLOR_RGB2HLS_FULL)


def rgb2hsv(image):
    return cv.cvtColor(image, cv.COLOR_RGB2HSV)


def rgb2hsv_full(image):
    return cv.cvtColor(image, cv.COLOR_RGB2HSV_FULL)


def rgb2lab(image):
    return cv.cvtColor(image, cv.COLOR_RGB2LAB)


def rgb2luv(image):
    return cv.cvtColor(image, cv.COLOR_RGB2LUV)


def rgb2lab1(image):
    return cv.cvtColor(image, cv.COLOR_RGB2Lab)


def rgb2luv1(image):
    return cv.cvtColor(image, cv.COLOR_RGB2Luv)


def rgb2rgba(image):
    return cv.cvtColor(image, cv.COLOR_RGB2RGBA)


def rgb2xyz(image):
    return cv.cvtColor(image, cv.COLOR_RGB2XYZ)


def rgb2ycr_cb(image):
    return cv.cvtColor(image, cv.COLOR_RGB2YCR_CB)


def rgb2ycr_cb1(image):
    return cv.cvtColor(image, cv.COLOR_RGB2YCrCb)


def rgb2ycr_yuv(image):
    return cv.cvtColor(image, cv.COLOR_RGB2YUV)


def rgb2yuv_i420(image):
    return cv.cvtColor(image, cv.COLOR_RGB2YUV_I420)


def rgb2yuv_iyuv(image):
    return cv.cvtColor(image, cv.COLOR_RGB2YUV_IYUV)


def rgb2yv12(image):
    return cv.cvtColor(image, cv.COLOR_RGB2YUV_YV12)


if __name__ == '__main__':
    flags = [i for i in dir(cv) if i.startswith('COLOR')]
    print(flags)
