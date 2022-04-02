import cv2
import numpy as np
import math
import sys
import os.path

winoffsetx = 210
winoffsety = 230
width = 0
height = 0

colours = {}

def add(name, r, g, b):
    colours[name] = [r,g,b]

add("maroon", 128,0,0)
add("dark red", 139,0,0)
add("brown", 165,42,42)
add("firebrick", 178,34,34)
add("crimson", 220,20,60)
add("red", 255,0,0)
add("coral", 255,127,80)
add("indian red", 205,92,92)
add("light coral", 240,128,128)
add("orange red", 255,69,0)
add("dark orange", 255,140,0)
add("orange", 255,165,0)
add("gold", 255,215,0)
add("dark khaki", 189,183,107)
add("khaki", 240,230,140)
add("olive", 128,128,0)
add("yellow", 255,255,0)
add("yellow green", 154,205,50)
add("dark olive green", 85,107,47)
add("olive drab", 107,142,35)
add("lawn green", 124,252,0)
add("chart reuse", 127,255,0)
add("green yellow", 173,255,47)
add("dark green", 0,100,0)
add("green", 0,128,0)
add("forest green", 34,139,34)
add("lime", 0,255,0)
add("lime green", 50,205,50)
add("light green", 144,238,144)
add("pale green", 152,251,152)
add("dark sea green", 143,188,143)
add("spring green", 0,255,127)
add("medium aqua marine", 102,205,170)
add("medium sea green", 60,179,113)
add("light sea green", 32,178,170)
add("dark slate gray", 47,79,79)
add("teal", 0,128,128)
add("dark cyan", 0,139,139)
add("aqua", 0,255,255)
add("cyan", 0,255,255)
add("light cyan", 224,255,255)
add("dark turquoise", 0,206,209)
add("turquoise", 64,224,208)
add("pale turquoise", 175,238,238)
add("aqua marine", 127,255,212)
add("deep sky blue", 0,191,255)
add("light blue", 173,216,230)
add("sky blue", 135,206,235)
add("light sky blue", 135,206,250)
add("midnight blue", 25,25,112)
add("navy", 0,0,128)
add("dark blue", 0,0,139)
add("blue", 0,0,255)
add("royal blue", 65,105,225)
add("blue violet", 138,43,226)
add("indigo", 75,0,130)
add("dark slate blue", 72,61,139)
add("slate blue", 106,90,205)
add("dark magenta", 139,0,139)
add("dark violet", 148,0,211)
add("purple", 128,0,128)
add("thistle", 216,191,216)
add("violet", 238,130,238)
add("magenta", 255,0,255)
add("orchid", 218,112,214)
add("deep pink", 255,20,147)
add("light pink", 255,182,193)
add("pink", 255,192,203)
add("antique white", 250,235,215)
add("beige", 245,245,220)
add("wheat", 245,222,179)
add("light yellow", 255,255,224)
add("saddle brown", 139,69,19)
add("chocolate", 210,105,30)
add("tan", 210,180,140)
add("slate gray", 112,128,144)
add("light slate gray", 119,136,153)
add("lavender", 230,230,250)
add("ivory", 255,255,240)
add("azure", 240,255,255)
add("black", 0,0,0)
add("dim grey", 105,105,105)
add("grey", 128,128,128)
add("dark grey", 169,169,169)
add("silver", 192,192,192)
add("light grey", 211,211,211)
add("white", 255,255,255)


def inside(mouseX, mouseY):
    return (mouseX < winoffsetx + width and mouseX > winoffsetx and mouseY < winoffsety + height and mouseY > winoffsety)

def relativePositions(mouseX, mouseY):
    mouseX -= winoffsetx
    mouseY -= winoffsety

    if mouseX < 0:
        mouseX = 0
    if mouseX >= width:
        mouseX = width-1
    if mouseY < 0:
        mouseY = 0
    if mouseY >= height:
        mouseY = height-1
    
    return pyautogui.Point(mouseX, mouseY)

def findClosest(r, g, b):
    # 3D vectors
    colour = ""
    min = 1000000;
    for i in colours.keys():
        dr = r-colours[i][0]
        dg = g-colours[i][1]
        db = b-colours[i][2]
        distance = math.sqrt(dr*dr + dg*dg + db*db)
        if distance < min:
            min = distance
            colour = i
    return colour

def crosshair(mouseX, mouseY, frame):
    for k in range(mouseX-10, mouseX+10):
        if k >= 0 and k < width:
            frame[mouseY][k][2] = 255
            frame[mouseY][k][1] = 0
            frame[mouseY][k][0] = 0
    for k in range(mouseY-10, mouseY+10):
        if k >= 0 and k < height:
            frame[k][mouseX][2] = 255
            frame[k][mouseX][1] = 0
            frame[k][mouseX][0] = 0

def drawAddit(frame, r, g, b, text):
    cv2.rectangle(frame, (10,height - 70), (70,height-10), (0,0,0),-1)
    cv2.rectangle(frame, (12,height - 68), (68,height-12), (int(r),int(g),int(b)),-1)
    cv2.putText(frame, text, (80,height-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    crosshair(mouseX, mouseY, frame)

fr = 0
fb = 0
fg = 0
fcolour = ""
mouseX = 0
mouseY = 0

path = input("Insert path: ")
if not os.path.isfile(path):
    print("Invalid path")
    exit()

def onMouse(event,x,y,flags,param):
    global mouseX, mouseY
    mouseX = x
    mouseY = y
    
cv2.namedWindow('ColorTellingAssistant', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('ColorTellingAssistant',onMouse)

while True:
    frame = cv2.imread(path)

    # Get frame dimensions
    dim=frame.shape

    width = dim[1]
    height = dim[0]
    fr = frame[mouseY][mouseX][0]
    fg = frame[mouseY][mouseX][1]
    fb = frame[mouseY][mouseX][2]
    fcolour = findClosest(fb,fg,fr)

    drawAddit(frame, fr, fg, fb, fcolour)
    
    cv2.imshow('ColorTellingAssistant', frame)

    k = cv2.waitKey(1) & 0xFF
    if not cv2.getWindowProperty('ColorTellingAssistant', cv2.WND_PROP_VISIBLE):
        break
    if k == 27:  # Key code for ESC
        break 
# Destroy all the windows
cv2.destroyAllWindows()
