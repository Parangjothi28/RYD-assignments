import cv2
import numpy as np

# Load image and remove watermark
img = cv2.imread('inp.png')
alpha = 2.5
beta = -160
new = alpha * img + beta
new = np.clip(new, 0, 255).astype(np.uint8)

# Grayscale, Gaussian blur and Filter2D, Otsu's threshold of Image
gs = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gs, (7,7), 0)

# ALternate blurring to blur more
kernel2 = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(gs,-1,kernel2)

thresh = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Create rectangular structuring element and dilate
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
dilate = cv2.dilate(thresh, kernel, iterations=6)

# Find contours and draw rectangle
contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    # Ignoring smaller rectangles
    if w*h > 2000:
        cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 2)

cv2.imshow('thresh', thresh)
cv2.imshow('dilate', dilate)
cv2.imshow('image', img)
cv2.imwrite('output.png',img)
cv2.waitKey()
