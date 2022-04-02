#import the libraries
import cv2 as cv
import numpy as np

import tkinter as tk
from tkinter.colorchooser import askcolor

root = tk.Tk()
root.title('Color Chooser')
root.geometry('300x150')

def change_color():
    colors = askcolor(title="Tkinter Color Chooser")
    root.configure(bg=colors[1])
    global accent_color
    accent_color=colors[1]
    root.quit()

tk.Button(
    root,
    text='Select a Color',
    command=change_color).pack(expand=True)

#main loop of color chooser and path specifier
root.mainloop()

def hex_to_rgb(num):
    num=num[1:]
    return tuple(int(num[i:i+2], 16) for i in (0, 2, 4))

#read the image
path=input("Choose image path: ")
img = cv.imread(path)
#convert the BGR image to HSV colour space
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#obtain the grayscale image of the original image
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#set the bounds for the red hue
lower_red = np.array([0,0,0])
upper_red = np.array(hex_to_rgb(accent_color))

#create a mask using the bounds set
mask = cv.inRange(hsv, lower_red, upper_red)
#create an inverse of the mask
mask_inv = cv.bitwise_not(mask)
#Filter only the red colour from the original image using the mask(foreground)
res = cv.bitwise_and(img, img, mask=mask)
#Filter the regions containing colours other than red from the grayscale image(background)
background = cv.bitwise_and(gray, gray, mask = mask_inv)
#convert the one channelled grayscale background to a three channelled image
background = np.stack((background,)*3, axis=-1)
#add the foreground and the background
added_img = cv.add(res, background)

#create resizable windows for the images
cv.namedWindow("added", cv.WINDOW_NORMAL)

#display the images
cv.imshow("added",added_img)

if cv.waitKey(0):
    cv.destroyAllWindows()