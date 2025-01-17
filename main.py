import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize video capture, Mediapipe hands, and PyAutoGUI
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Variables for smoothing
prev_index_x, prev_index_y = 0, 0
smoothing_factor = 0.7

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror the frame
    frame_height, frame_width, _ = frame.shape

    # Convert to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            # Get coordinates of the index finger tip (id = 8) and thumb tip (id = 4)
            index_finger_tip = landmarks[8]
            thumb_tip = landmarks[4]

            # Convert normalized coordinates to screen coordinates
            index_x = int(index_finger_tip.x * screen_width)
            index_y = int(index_finger_tip.y * screen_height)
            thumb_x = int(thumb_tip.x * screen_width)
            thumb_y = int(thumb_tip.y * screen_height)

            # Apply smoothing to cursor movement
            smoothed_x = prev_index_x * smoothing_factor + index_x * (1 - smoothing_factor)
            smoothed_y = prev_index_y * smoothing_factor + index_y * (1 - smoothing_factor)

            prev_index_x, prev_index_y = smoothed_x, smoothed_y

            # Move the mouse to the smoothed index finger position
            pyautogui.moveTo(smoothed_x, smoothed_y)

            # Draw circles at index and thumb tips
            cv2.circle(frame, (int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)), 10, (0, 255, 255), -1)
            cv2.circle(frame, (int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)), 10, (255, 0, 255), -1)

            # Check distance between index and thumb for clicking
            distance = np.hypot(thumb_x - index_x, thumb_y - index_y)
            if distance < 50:  # Adjust threshold for clicking
                pyautogui.click()
                cv2.putText(frame, "Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the video feed
    cv2.imshow('Virtual Mouse', frame)

    # Exit on pressing 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
