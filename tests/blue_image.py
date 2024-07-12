import numpy as np
import cv2 as cv

img = cv.imread("./assets/fll_robot.png")

blue_overlay = np.full(img.shape, (255, 0, 0), dtype=np.uint8)

bluer_image = cv.addWeighted(img, 0.5, blue_overlay, 0.5, 0)

cv.imwrite("./assets/fll_robot_blue.png", bluer_image)
cv.waitKey(0)
