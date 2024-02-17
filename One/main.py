import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from Guassian_Blur import gaussian_blur2
from Sobel_Filter import sobel_filter
from Non_Maximum_Suppression import non_maximum_suppression
from Thresholding import threshold

if __name__ == '__main__':
    img = Image.open('.\images\GrenoraCropped.jpg') 
    # now relative address, still need to find way to not hard-code what image
    gray = np.array(img.convert('L'))
    blur = gaussian_blur2(gray, 1, (40, 40))
    # Might need to change sigma to 1, the image might still be too blurry
    gradient, theta = sobel_filter(blur, 1.5, (10, 10))
    nms = non_maximum_suppression(gradient, theta)
    th = threshold(nms, 0.05, 0.09)

    plt.figure()
    plt.imshow(nms, cmap='gray')
    plt.show()