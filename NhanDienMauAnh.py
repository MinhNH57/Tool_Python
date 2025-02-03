import cv2
import numpy as np

# Đọc ảnh
image_path = 'C:/Users/Dell/Pictures/Screenshots/Screenshot 2024-12-23 113425.png'  
image = cv2.imread(image_path)

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

lower_orange = np.array([5, 150, 150])  
upper_orange = np.array([25, 255, 255])

lower_green = np.array([35, 100, 100])  
upper_green = np.array([85, 255, 255])

mask1_red = cv2.inRange(hsv_image, lower_red1, upper_red1)
mask2_red = cv2.inRange(hsv_image, lower_red2, upper_red2)

mask_orange = cv2.inRange(hsv_image, lower_orange, upper_orange)

mask_green = cv2.inRange(hsv_image, lower_green, upper_green)

mask = mask1_red | mask2_red | mask_orange | mask_green

result = cv2.bitwise_and(image, image, mask=mask)

cv2.imshow('Ảnh gốc', image)
cv2.imshow('Nhận diện màu', result)

cv2.waitKey(0)
cv2.destroyAllWindows()
