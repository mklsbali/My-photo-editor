import cv2 as cv


def bgr2rgb(image):
    return cv.cvtColor(image, cv.COLOR_BGR2RGB)


def bgr2bgr555(image):
    return cv.cvtColor(image, cv.COLOR_BGR2BGR555)


def bgr2bgr565(image):
    return cv.cvtColor(image, cv.COLOR_BGR2BGR565)


def bgr2bgra(image):
    return cv.cvtColor(image, cv.COLOR_BGR2BGRA)


def bgr2gray(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)


def bgr2hls(image):
    return cv.cvtColor(image, cv.COLOR_BGR2HLS)


def bgr2hls_full(image):
    return cv.cvtColor(image, cv.COLOR_BGR2HLS_FULL)


def bgr2hsv(image):
    # aux = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    return cv.cvtColor(image, cv.COLOR_BGR2HSV)


def bgr2hsv_full(image):
    return cv.cvtColor(image, cv.COLOR_BGR2HSV_FULL)


def bgr2lab(image):
    return cv.cvtColor(image, cv.COLOR_BGR2LAB)


def bgr2luv(image):
    return cv.cvtColor(image, cv.COLOR_BGR2LUV)


def bgr2lab1(image):
    return cv.cvtColor(image, cv.COLOR_BGR2Lab)


def bgr2luv1(image):
    return cv.cvtColor(image, cv.COLOR_BGR2Luv)


def bgr2rgba(image):
    return cv.cvtColor(image, cv.COLOR_BGR2RGBA)


def bgr2xyz(image):
    return cv.cvtColor(image, cv.COLOR_BGR2XYZ)


def bgr2ycr_cb(image):
    return cv.cvtColor(image, cv.COLOR_BGR2YCR_CB)


def bgr2ycr_cb1(image):
    return cv.cvtColor(image, cv.COLOR_BGR2YCrCb)


def bgr2ycr_yuv(image):
    return cv.cvtColor(image, cv.COLOR_BGR2YUV)


def bgr2yuv_i420(image):
    return cv.cvtColor(image, cv.COLOR_BGR2YUV_I420)


def bgr2yuv_iyuv(image):
    return cv.cvtColor(image, cv.COLOR_BGR2YUV_IYUV)


def bgr2yv12(image):
    return cv.cvtColor(image, cv.COLOR_BGR2YUV_YV12)


if __name__ == '__main__':
    flags = [i for i in dir(cv) if i.startswith('COLOR_BGR2')]
    print(flags)
