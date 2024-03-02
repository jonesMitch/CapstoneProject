import numpy as np
from Guassian_Blur import convolution

def sobel_filter(img: np.ndarray, sigma: int | float, filter_shape: int):
    xKernel = np.array(
        [[-1, 0, 1],
         [-2, 0, 2],
         [-1, 0, 1]]
    )
    yKernel = np.array(
        [[1, 2, 1],
         [0, 0, 0],
         [-1, 0, 1]]
    )

    xImg = convolution(img, xKernel)
    yImg = convolution(img, yKernel)

    gradient = np.hypot(xImg, yImg)
    gradient = gradient / gradient.max() * 255
    theta = np.arctan2(yImg, xImg)
    return np.squeeze(gradient), np.squeeze(theta)