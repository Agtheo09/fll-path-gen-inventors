import cv2 as cv


def handler(event, x, y, flags, param):
    print(x, y)


def crop(img, pt1, pt2):
    return img[pt1[1] : pt2[1], pt1[0] : pt2[0]]


raw = cv.imread("./test_2.jpg")

img = crop(raw, (110, 195), (1295, 875))

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
inverted_gray = cv.bitwise_not(gray)
_, binary = cv.threshold(inverted_gray, 15, 255, cv.THRESH_BINARY)
contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contour = max(contours, key=cv.contourArea)
x, y, w, h = cv.boundingRect(contour)

cv.rectangle(raw, (x + 110, y + 195), (x + 110 + w, y + 195 + h), (0, 255, 0), 1)

cv.imshow("Field", raw)
cv.setMouseCallback("Field", handler)
pad = -1
cv.imwrite("./field_2.jpg", crop(img, (x - pad, y - pad), (x + w + pad, y + h + pad)))
cv.waitKey(0)
cv.destroyAllWindows()
