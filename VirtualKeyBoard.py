
import cv2
import numpy as np
import pyautogui

# Define the colors for color segmentation (in HSV format)
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([30, 255, 255])

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the yellow color
    mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Get the largest contour (the hand)
        max_contour = max(contours, key=cv2.contourArea)

        # Get the bounding rectangle for the hand
        x, y, w, h = cv2.boundingRect(max_contour)

        # Calculate the area of the hand
        area = cv2.contourArea(max_contour)

        # Check if the area is increasing (gesture for click)
        if area > 10000:
            pyautogui.click()  # Perform a click action

        # Draw a rectangle around the hand
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Virtual Keyboard', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
