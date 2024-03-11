import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import cv2
import pytesseract

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
        left = width * .30
        top = 0
        right = width * .70
        bottom = height * .85
        cmg = img.crop((left, top, right, bottom))
        gray = np.array(cmg.convert('L'))
        blur = gaussian_blur2(gray, 1, (40, 40))
        # Might need to change sigma to 1, the image might still be too blurry
        gradient, theta = sobel_filter(blur, 1.5, (10, 10))
        nms = non_maximum_suppression(gradient, theta)
        th = threshold(nms, 0.05, 0.09)

        plt.figure()
        plt.title(filename + ' Final Result')
        plt.imshow(nms, cmap='gray')
        plt.show(block=True)
        
    #img = Image.open('.\images\GrenoraCropped.jpg')
    #pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    #img = Image.open('./images/testimage.jpg') 
    
    # now relative address, still need to find way to not hard-code what image
    #gray = np.array(img.convert('L'))
    #blur = gaussian_blur2(gray, 1, (40, 40))
    # Might need to change sigma to 1, the image might still be too blurry
    #gradient, theta = sobel_filter(blur, 1.5, (10, 10))
    #nms = non_maximum_suppression(gradient, theta)
    #th = threshold(nms, 0.05, 0.09)

    # i commented out some stuff just to test various things
    #plt.figure()
    #plt.imshow(nms, cmap='gray')
    #plt.show()

    #pytesseract below?
    #data = pytesseract.image_to_string(img, lang='eng',config='--psm 6')
    #print(data)

    #img2 = cv2.imread('./images/GrenoraCropped.jpg')
    #text = pytesseract.image_to_string(img2)
    #print(text)
