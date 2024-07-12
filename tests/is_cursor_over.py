import cv2 as cv
import numpy as np
import math

theta = 30

off = -300


def check(x, y):
    corners = [(0, 200), (200, 600), (600, 400), (400, 0)]

    poly = np.array(corners, dtype=np.int32)
    in_rect = cv.pointPolygonTest(poly, (x, y), False) >= 0

    cv.circle(
        white_mat, (int(x), int(y)), 2, (0, 255, 0) if in_rect else (0, 0, 255), -1
    )
    cv.imshow("view", white_mat)


def mouse_click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        check(x, y)


viewport_size = (600, 600)

white_mat = np.ones((viewport_size[1], viewport_size[0], 3), np.uint8) * 220

cv.line(white_mat, (0, 200), (400, 0), (0, 0, 0), 2)
cv.line(white_mat, (0, 200), (200, 600), (0, 0, 0), 2)
cv.line(white_mat, (200, 600), (600, 400), (0, 0, 0), 2)
cv.line(white_mat, (600, 400), (400, 0), (0, 0, 0), 2)

cv.imshow("view", white_mat)
cv.setMouseCallback("view", mouse_click)

for i in range(0, 600, 5):
    for j in range(0, 600, 5):
        check(i, j)

cv.waitKey(0)
cv.destroyAllWindows()
