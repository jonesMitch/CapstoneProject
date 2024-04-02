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

def getSlope(x1, y1, x2, y2):
    if(x2-x1 == 0):
        return 1
    else:
        return (y2-y1)/(x2-x1)
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
    #Straight line and we do not need to normalize
    if(x2-x1 == 0 or y2-y1 == 0):
        return x1, y1, x2, y2
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

    srcD = '.\images\\'
    for file in os.scandir(srcD):
        filename = file.path
        print(filename)
        img = cv2.imread(filename)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        saveName = file.name.removesuffix('.jpg')

        #Color HSV values: Blue 96-116, Orange 2-22, Green 53-73, light green 30-50
        #lower bound found by getting the HSV value of rgb then dividing the h by 2 and subtracting 10 the s and v are the standard
        lower_blue = np.array([2, 100, 20])
        #Upper bound found by getting the HSV value of rgb then dividing the h by 2 and Adding 10 the s and v are the standard
        upper_blue = np.array([22, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        kernel = np.ones((5,5), np.uint8)
        
        
        erosion = cv2.erode(mask, kernel, iterations = 3)
        dilation = cv2.dilate(erosion, kernel, iterations = 3)
        
        blur = cv2.GaussianBlur(erosion, (5, 5), 5)

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
                if(x1 < 0):
                    x1 = 0
                if(x2 < 0):
                    x2 = 0
                if(y1 < 0):
                    y1 = 0
                if(y2 < 0):
                    y2 = 0
                if (getSlope(x1, y1, x2, y2) < -0.5 or 0.5 < getSlope(x1, y1, x2, y2)):
                    minX = min(minX, x1, x2)
                    maxX = max(maxX, x1, x2)

                    print(x1.__str__() + ' ' + y1.__str__() + ' ' + x2.__str__() + ' ' + y2.__str__())
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            #print(minX.__str__() + maxX.__str__())
            crop = img[0:img.shape[0], minX:maxX]
            cv2.imwrite(saveName + '\Crop.jpg', crop)

        cv2.imwrite(saveName + '\Mask.jpg', mask)
        cv2.imwrite(saveName + '\Canny.jpg', canny)
        cv2.imwrite(saveName + '\Lines.jpg', img)
        cv2.imwrite(saveName + '\Image.jpg', hsv)
        cv2.imwrite(saveName + '\Blur.jpg', blur)
        cv2.imwrite(saveName + '\Erosion.jpg', erosion)
        cv2.imwrite(saveName + '\Dilation.jpg', dilation)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
