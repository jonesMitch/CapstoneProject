import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import pytesseract
from PIL import Image

from Guassian_Blur import gaussian_blur2
from Sobel_Filter import sobel_filter
from Non_Maximum_Suppression import non_maximum_suppression
from Thresholding import threshold

import requests
from bs4 import BeautifulSoup

# relevant URLs
# https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Fargo_NE_SnowStake.jpg
# https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Clyde_NW_SnowStake.jpg
# https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Clyde_South_SnowStake.jpg
# https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Ray_SE_SnowStake.jpg
# https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Prosper_South_SnowStake.jpg
# https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Prosper_NE_SnowStake.jpg
#
def getYintercept(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    b = y1 - m*(x1)
    return b
def getXintercept(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    b = y1 - m*(x1)
    xint = -b/m
    return xint
def getBLine(x1, y1, x2, y2):
    yint = getYintercept(x1, y1, x2, y2)
    xint = getXintercept(x1, y1, x2, y2)
    if x1 < 0:
        x1 = 0
        y1 = yint
    if y1 < 0:
        y1 = 0
        x1 = xint
    if x2 < 0:
        x2 = 0
        y2 = yint
    if y2 < 0:
        y2 = 0
        x2 = xint
    return x1, y1, x2, y2

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    #path always needed when using tesseract
    #scrape for station here
    #scrape for image here
    srcD = '.\images\\'
    for file in os.scandir(srcD):
        filename = file.path
        print(filename)
        img = cv2.imread(filename)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        #lower bound found by getting the HSV value of rgb then dividing the h by 2 and subtracting 10 the s and v are the standard 96
        lower_blue = np.array([96, 100, 20])
        #Upper bound found by getting the HSV value of rgb then dividing the h by 2 and Adding 10 the s and v are the standard 116
        upper_blue = np.array([116, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        kernel = np.ones((5,5), np.uint8)
        
        dilation = cv2.dilate(mask, kernel, iterations = 1)
        erosion = cv2.erode(dilation, kernel, iterations = 2)
        dilation = cv2.dilate(erosion, kernel, iterations = 1)
        
        blur = cv2.GaussianBlur(erosion, (0, 0), 5)

        canny = cv2.Canny(blur, 50, 150)
        lines = cv2.HoughLines(canny, 1, np.pi / 180, 200)
        

        if lines is not None:
            minX = 1000000
            maxX = 0
            for line in lines:
                rho,theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                lne = getBLine(x1, y1, x2, y2)
                x1 = int(lne[0])
                y1 = int(lne[1])
                x2 = int(lne[2])
                y2 = int(lne[3])

                minX = min(minX, x1, x2)
                maxX = max(maxX, x1, x2)

                print(x1.__str__() + ' ' + y1.__str__() + ' ' + x2.__str__() + ' ' + y2.__str__())
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            crop = img[0:img.shape[0], minX:maxX]
            cv2.imshow('Crop', crop)

        
        
        #cv2.imshow('Canny', canny)        
        #cv2.imshow('Mask', mask)
        #cv2.imshow('Lines', img)
        #cv2.imshow('Image', hsv)
        #cv2.imshow('Blur', blur)
        #cv2.imshow('Erosion', erosion)
        #cv2.imshow('Dilation', dilation)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        data = pytesseract.image_to_string(mask, lang='eng',config='--psm 6')
        nums = data.lower().translate({ord(i): None for i in 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()-_+=/:;".,<>?—~|\[]{} \''})
        #stupid hardcoding here to remove all non-number characters from string
        print(nums)
        
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
    #plt.show(block=True)
        
    #contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(img, contours, -1, (0,255,0), 3)
    #cv2.imshow('contours', img)