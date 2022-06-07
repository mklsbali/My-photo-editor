import cython

@cython.boundscheck(False)
cpdef unsigned char[:, :, :] test_filter(unsigned char [:, :, :] image, int r, int g, int b):
    cdef int width, height, i, j
    rgb_color = (r, g, b)
    width = image.shape[1]
    height = image.shape[0]
    for j in range(0, height):
        for i in range(0, width):
            image[j, i, 0] = image[j, i, 0] + rgb_color[0] /2
            image[j, i, 1] = image[j, i, 1] + rgb_color[1] /2
            image[j, i, 2] = image[j, i, 2] + rgb_color[2] /2

    return image
