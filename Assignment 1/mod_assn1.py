import numpy as np
import cv2

img = cv2.imread("inp.png")
alpha = 2.5
beta = -160
new = alpha * img + beta
new = np.clip(new, 0, 255).astype(np.uint8)

imgc = img.copy()
edges = cv2.Canny(img,180,200,apertureSize = 3)
minLineLength=50
lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=215, minLineLength=minLineLength)
x11,y11=0,0
miny = 100000
maxy = -100
maxx = -100
n1 = 0
n2 = 0
m1 = 0
m2 = 0
#print(len(lines))
for i in range(len(lines)-1):
    x1, y1, x2, y2 = lines[i][0]
    #print(x1,y1)
    #Checking for horizontal line. Here, we focus on vertical lines.
    if(x1!=x2):
        #print(x2-x1)
        if y1 == y2:
            if y1 > maxy and x2-x1 > 200:
                maxy = y1
            if y1 < miny and x2-x1 > 200:
                miny = y1
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        continue

x1 = 0
x2 = img.shape[1]
y1 = 0
y2 = miny
cv2.rectangle(new,(x1,y1),(x2,y2),(255,255,255),-1)
x1 = 0
y1 = maxy
x2 = img.shape[1]
y2 = img.shape[0]
cv2.rectangle(new,(x1,y1),(x2,y2),(255,255,255),-1)


gs = cv2.cvtColor(new[miny:maxy,:], cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gs, (31,131), 0)

# ALternate blurring to blur more
kernel2 = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(gs,-1,kernel2)

thresh = cv2.threshold(blur, 0, 245, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
row,cols = thresh.shape
print(row,cols)

# Create rectangular structuring element and dilate
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(thresh, kernel, iterations=3)

# Find contours and draw rectangle
contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
tot_cols = 0
print(maxy-miny)
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    # if w*h > 2000 and h > 40:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 2)
    #print(h)
    if h == maxy-miny:
        tot_cols += 1

print(tot_cols)

part_wid = cols//tot_cols

for i in range(tot_cols):
    start = i*part_wid
    fin = (i+1)*part_wid
    blurry = cv2.GaussianBlur(gs[:,start:fin],(21,21),0)
    thresh = cv2.threshold(blurry, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilate = cv2.dilate(thresh, kernel, iterations=5)

    contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        if w*h > 2000 and h > 40:
            cv2.rectangle(imgc,(start,y+miny),(fin,y+miny+h),(0,255,0),2)
    cv2.imshow('thresh', thresh)
    cv2.imshow('dilate', dilate)
cv2.imwrite('modoutput.png',imgc)
cv2.imshow('img2',imgc)
cv2.waitKey()

cv2.waitKey()

