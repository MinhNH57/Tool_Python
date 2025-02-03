import cv2 
import numpy as np 

video_cam = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow("AdjustBar")
cv2.createTrackbar("L-H", "AdjustBar", 0, 100, nothing)
cv2.createTrackbar("L-S", "AdjustBar", 66, 255, nothing)
cv2.createTrackbar("L-V", "AdjustBar", 134, 255, nothing)
cv2.createTrackbar("U-H", "AdjustBar", 180, 180, nothing)
cv2.createTrackbar("U-S", "AdjustBar", 255, 255, nothing)
cv2.createTrackbar("U-V", "AdjustBar", 243, 255, nothing)

while True:
    _, frame = video_cam.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "AdjustBar")
    l_s = cv2.getTrackbarPos("L-S", "AdjustBar")
    l_v = cv2.getTrackbarPos("L-V", "AdjustBar")

    u_h = cv2.getTrackbarPos("U-H", "AdjustBar")
    u_s = cv2.getTrackbarPos("U-S", "AdjustBar")
    u_v = cv2.getTrackbarPos("U-V", "AdjustBar")

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), dtype=np.uint8)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.022 * cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 450:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            if len(approx) == 3:
                cv2.putText(frame, "Tam Giac", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
            elif len(approx) == 4:
                cv2.putText(frame, "Hinh chu nhat (Hinh vuong)", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
            elif len(approx) > 5:
                cv2.putText(frame, "Hinh tron", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

    cv2.imshow("Mask", mask)
    cv2.imshow("Nhan dien", frame)

    # Dừng khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_cam.release()
cv2.destroyAllWindows()
