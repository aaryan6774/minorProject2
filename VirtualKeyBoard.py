# import cv2
# import numpy as np
# import math
#
# # Define the letters on the keyboard
# keys = ['A', 'B', 'C']
#
# # Define the positions of the keys
# key_positions = [(50, 50), (150, 50), (250, 50)]
#
# # Initialize the selected key
# selected_key = None
#
# # Function to detect if a point is inside a circle
# def point_inside_circle(point, center, radius):
#     return math.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2) <= radius
#
# # Create a black image as the background
# img = np.zeros((300, 400, 3), np.uint8)
#
# while True:
#     # Display the keyboard
#     for i, key in enumerate(keys):
#         color = (255, 255, 255) if selected_key == i else (100, 100, 100)
#         cv2.circle(img, key_positions[i], 30, color, -1)
#         cv2.putText(img, key, (key_positions[i][0] - 10, key_positions[i][1] + 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
#
#     cv2.imshow('Keyboard', img)
#
#     # Wait for key press
#     key = cv2.waitKey(1) & 0xFF
#
#     # Reset the selected key
#     selected_key = None
#
#     # Get the position of the mouse click
#     if cv2.getWindowProperty('Keyboard', cv2.WND_PROP_VISIBLE) < 1:
#         break
#
#     if cv2.getWindowProperty('Keyboard', cv2.WND_PROP_AUTOSIZE) != cv2.WINDOW_FULLSCREEN:
#         _, _, w, h = cv2.getWindowImageRect('Keyboard')
#         if w == 0 or h == 0:
#             break
#
#     if key == ord('q'):
#         break
#     elif key == ord('a') or key == ord('b') or key == ord('c'):
#         selected_key = key - ord('a')
#
# cv2.destroyAllWindows()



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
