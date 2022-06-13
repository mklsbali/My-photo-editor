import cython
import numpy as np

@cython.boundscheck(False)
cpdef unsigned char[:, :, :] test_filter(unsigned char [:, :, :] image, rgb):
    cdef int width, height, i, j, k, c, r, g, b
    r = rgb[2]
    g = rgb[1]
    b = rgb[0]
    rgb_color = (r, g, b)
    width = image.shape[1]
    height = image.shape[0]
    empty_array = np.empty([height, width, 3])
    for j in range(0, height):
        for i in range(0, width):
            for k in range(0, 3):
                c = (image[j, i, k] + rgb_color[k])%255 / 2
                image[j, i, k] = c




    return image

