import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

MAX_VALUE = 46
# 1 for left / right tick marks, 0 for middle tick marks
TICK_MARKS = 1

path = '.\cropped\GrenoraCropped.jpg'
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

edges = cv2.Canny(img, 299, 300)

if (TICK_MARKS == 0):
    x = len(edges[0]) / 2
elif (TICK_MARKS == 1):
    x = (len(edges[0]) / 4) * 3
else:
    print("Wrong value for tick marks")

x = int(x)

counter = 0
for y in range(0, len(edges)):
    if edges[y][x] == 255:
        counter += 1

# This just shows the row of pixels that are counted along
for y in range(0, len(edges)):
    for x2 in range(x-2, x+2):
        edges[y][x2] = 255

counter /= 2
counter = math.floor(counter)
print(f'Snow height is {MAX_VALUE - (counter * 2)} inches')

plt.figure()
plt.imshow(edges, cmap='gray')
plt.show()