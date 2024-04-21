import cv2
import numpy as np
import math
import pyautogui

cap = cv2.VideoCapture(0)

top, right, bottom, left = 100, 300, 300, 500

prev_avg_x, prev_avg_y = 0, 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    hand_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10000:
            hand_contour = contour
            break

    if hand_contour is not None:
        M = cv2.moments(hand_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

            avg_x = (prev_avg_x + cx) / 2
            avg_y = (prev_avg_y + cy) / 2

            if avg_x < left:
                pyautogui.press('volumeup')
            elif avg_x > right:
                pyautogui.press('volumedown')

            prev_avg_x, prev_avg_y = avg_x, avg_y

    cv2.imshow("Frame", frame)

    # 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
