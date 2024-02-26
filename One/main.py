import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

from Guassian_Blur import gaussian_blur2
from Sobel_Filter import sobel_filter
from Non_Maximum_Suppression import non_maximum_suppression
from Thresholding import threshold

if __name__ == '__main__':
    srcD = '.\images\\'
    for file in os.scandir(srcD):
        filename = file.path
        print(filename)
        img = Image.open(filename)
        width, height = img.size
        print(str(width) + " " + str(height) + " " + str(img.size))
        left = width * .25
        top = 0
        right = width * .75
        bottom = height
        cmg = img.crop((left, top, right, bottom))
        #gray = np.array(cmg.convert('L'))
        #blur = gaussian_blur2(gray, 1, (40, 40))
        # Might need to change sigma to 1, the image might still be too blurry
        #gradient, theta = sobel_filter(blur, 1.5, (10, 10))
        #nms = non_maximum_suppression(gradient, theta)
        #th = threshold(nms, 0.05, 0.09)

        plt.imshow(cmg)
        plt.show(block=True)
        #plt.figure()
        #plt.imshow(nms, cmap='gray')
        #plt.show(block=True)
        
    #img = Image.open('.\images\GrenoraCropped.jpg')
    # now relative address, still need to find way to not hard-code what image
    #gray = np.array(img.convert('L'))
    #blur = gaussian_blur2(gray, 1, (40, 40))
    # Might need to change sigma to 1, the image might still be too blurry
    #gradient, theta = sobel_filter(blur, 1.5, (10, 10))
    #nms = non_maximum_suppression(gradient, theta)
    #th = threshold(nms, 0.05, 0.09)

    #plt.figure()
    #plt.imshow(nms, cmap='gray')
    #plt.show(True)