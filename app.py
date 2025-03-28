import cv2
import numpy as np
import pyautogui
import time

# Start Video Capture
cap = cv2.VideoCapture(0)

# Store previous state to avoid repeated key presses
prev_left_hand = False
prev_right_hand = False

# Cooldown timer to prevent rapid key presses
cooldown_time = 0.5  # Half a second delay
last_key_press_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Flip frame for natural movement
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Define column boundaries (1:1.5:1 ratio)
    left_boundary = int(w * 0.25)   # 25% width for left section
    right_boundary = int(w * 0.75)  # 75% width for right section

    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define skin color range (adjust if needed)
    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)

    # Create mask for skin color detection
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Ignore the center column
    mask[:, left_boundary:right_boundary] = 0  

    # Find contours (hands)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    left_hand_up = False
    right_hand_up = False

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:  # Filter out small noise
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2

            # Determine if hand is in left or right section (ignoring center)
            if center_x < left_boundary:  # Left section
                left_hand_up = center_y < frame.shape[0] // 2
            elif center_x > right_boundary:  # Right section
                right_hand_up = center_y < frame.shape[0] // 2

            # Draw rectangle around detected hand
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Only send keypress if state has changed and cooldown time has passed
    current_time = time.time()
    
    if left_hand_up and not prev_left_hand and (current_time - last_key_press_time > cooldown_time):
        print("Left Hand Up - Pressing SPACE")
        cv2.putText(frame, "Left Hand Up (Jump)", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        pyautogui.press('space')  # Jump
        last_key_press_time = current_time  # Reset cooldown
    
    if right_hand_up and not prev_right_hand and (current_time - last_key_press_time > cooldown_time):
        print("Right Hand Up - Pressing D")
        cv2.putText(frame, "Right Hand Up (Move Right)", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        pyautogui.press('d')  # Move Right
        last_key_press_time = current_time  # Reset cooldown

    if not right_hand_up and prev_right_hand and (current_time - last_key_press_time > cooldown_time):
        print("Right Hand Down - Pressing A")
        cv2.putText(frame, "Right Hand Down (Move Left)", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        pyautogui.press('a')  # Move Left
        last_key_press_time = current_time  # Reset cooldown

    # Update previous state
    prev_left_hand = left_hand_up
    prev_right_hand = right_hand_up

    # Draw boundary lines for debugging
    cv2.line(frame, (left_boundary, 0), (left_boundary, h), (0, 0, 255), 2)  # Left boundary
    cv2.line(frame, (right_boundary, 0), (right_boundary, h), (0, 0, 255), 2)  # Right boundary

    # Display the debug window
    cv2.imshow("Hand Gesture Controller", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
