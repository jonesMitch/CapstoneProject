import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import re
import pytesseract
import json

from PIL import Image
from One.Guassian_Blur import gaussian_blur2
from One.Sobel_Filter import sobel_filter
from One.Non_Maximum_Suppression import non_maximum_suppression
from One.Thresholding import threshold

import requests
from bs4 import BeautifulSoup

images_dir = ""

def parseConfig():
    configData
    with open("config.json", "r") as file:
        configData = json.load(file)
    images_dir = configData['one']['image_dir']

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

def main_run(color: int):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    srcD = '.\images\\'
    for file in os.scandir(srcD):
        filename = file.path
        print(filename)
        img = cv2.imread(filename)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        saveName = file.name.removesuffix('.jpg')

        #Color HSV values: Blue 96-116, Orange 2-22, Green 53-73, light green 30-50
        #lower bound found by getting the HSV value of rgb then dividing the h by 2 and subtracting 10 the s and v are the standard
        lower_color = np.array([2, 100, 20])
        #Upper bound found by getting the HSV value of rgb then dividing the h by 2 and Adding 10 the s and v are the standard
        upper_color = np.array([22, 255, 255])
        mask = cv2.inRange(hsv, lower_color, upper_color)

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

                    #print(x1.__str__() + ' ' + y1.__str__() + ' ' + x2.__str__() + ' ' + y2.__str__())
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

        hsvTess = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        tess = mask = cv2.inRange(hsvTess, lower_color, upper_color)
        data = pytesseract.image_to_string(tess, lang='eng',config='--psm 6') #using tesseract to get text recognition
        noLet = data.lower().translate({ord(i): None for i in 'abcdefghijklmnopqrstuvw‘xyz!@£”#$é%“^&*()-_+=/:;".,<>?—~|\°[]{} \''})
        nums = noLet.replace('\n', ' ').replace('\r', '')
        #hardcoding here to remove all non-number characters from string
        controlList = [30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        #control list is numbers that should be found on full snowstake
        numList = [] #empty list to represent numbers found on snowstake
        numList = (list(map(int, re.findall('\d+', nums)))) #find the numbers from a given string and add them to this list
        if not numList: #if the list is empty of elements go to manual evaluation
            print("Please manually evaluate at station: ")
            #Output data
            nameJson = saveName + "Data"
            data = {
                "station": saveName,
                "inches of snow": None,
                "needs review": True
            }
        else:
            depth = min(numList)
            print(numList)
            print(depth) #replace with functional list when working
            #Output data
            nameJson = saveName + "Data"
            data = {
                "station": saveName,
                "inches of snow": depth,
                "needs review": False
            }
        file = open(".\JSONs\\" + nameJson + ".json", "w")
        json.dump(data, file, indent=3)
        file.close()

def run():
    parseConfig()
    

'''
if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    img = Image.open('./images/testimage.jpg') 
    # now relative address, still need to find way to not hard-code what image
    gray = np.array(img.convert('L'))
    blur = gaussian_blur2(gray, 1, (40, 40))
    # Might need to change sigma to 1, the image might still be too blurry
    gradient, theta = sobel_filter(blur, 1.5, (10, 10))
    nms = non_maximum_suppression(gradient, theta)
    th = threshold(nms, 0.05, 0.09)

    # i commented out some stuff just to test various things
    #plt.figure()
    #plt.imshow(nms, cmap='gray')
    #plt.show()

    #pytesseract below?
    data = pytesseract.image_to_string(img, lang='eng',config='--psm 6')
    print(data)

    #img2 = cv2.imread('./images/GrenoraCropped.jpg')
    #text = pytesseract.image_to_string(img2)
    #print(text)

    #Output
    file = open(".\JSONs\\" + nameJson + ".json", "w")
    json.dump(data, file, indent=3)
    file.close()'''
