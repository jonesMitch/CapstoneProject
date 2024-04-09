import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def gaussian_blur(img: np.ndarray, sigma: int | float, shape: list | tuple):
    m, n = shape
    m_half = m // 2
    n_half = n // 2

    filter = np.zeros((m, n), np.float32)

    for y in range(-m_half, m_half):
        for x in range(-n_half, n_half):
            normal = 1 / (2.0 * np.pi * sigma**2.0)
            exp_term = np.exp(-(x**2.0 + y**2.0) / (2.0 * sigma**2.0))
            filter[y+m_half, x+n_half] = normal * exp_term
    blur = convolution(img, filter)
    return blur.astype(np.uint8)

def gaussian_blur2(img: np.ndarray, sigma: int | float, shape: list | tuple):
    filter = np.zeros((shape[0], shape[1]), np.float32)
    size_y = shape[0] // 2
    size_x = shape[1] // 2

    x, y = np.mgrid[-size_y:size_y+1, -size_x:size_x+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    filter = np.exp(-((x**2 + y**2) / (2.0 * sigma**2))) * normal

    return convolution(img, filter)

def convolution(image: np.ndarray, kernel: list | tuple) -> np.ndarray:
    if len(image.shape) == 3:
        m_i, n_i, c_i = image.shape
    else:
        image = image[..., np.newaxis]
        m_i, n_i, c_i = image.shape

    m_k, n_k = kernel.shape
    
    y_strides = m_i - m_k + 1
    x_strides = n_i - n_k + 1

    img = image.copy()
    output_shape = (y_strides, x_strides, c_i)
    output = np.zeros(output_shape, dtype=np.float32)

    output_tmp = output.reshape((output_shape[0]*output_shape[1], output_shape[2]))

    count = 0
    for i in range(y_strides):
        for j in range(x_strides):
            for c in range(c_i):
                sub_matrix = img[i:i+m_k, j:j+n_k, c]
                output_tmp[count, c] = np.sum(sub_matrix * kernel)
            count += 1
    return output_tmp.reshape(output_shape)