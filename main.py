<<<<<<< HEAD
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
=======
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import webview
import threading

# Initialize Mediapipe Hand Detector
hand_detector = mp.solutions.hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Variables for smoothing
prev_index_x, prev_index_y = 0, 0
smoothing_factor = 0.7
tracking = False  # Global flag for tracking
prev_click_time = 0  # For double-click detection


def start_camera():
    """Starts camera tracking when the button is clicked."""
    global tracking, prev_click_time
    tracking = True
    cap = cv2.VideoCapture(0)

    while tracking:
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
                middle_finger_tip = landmarks[12]  # Middle finger for scroll

                # Convert normalized coordinates to screen coordinates
                index_x = int(index_finger_tip.x * screen_width)
                index_y = int(index_finger_tip.y * screen_height)
                thumb_x = int(thumb_tip.x * screen_width)
                thumb_y = int(thumb_tip.y * screen_height)
                middle_y = int(middle_finger_tip.y * screen_height)

                # Apply smoothing to cursor movement
                global prev_index_x, prev_index_y
                smoothed_x = prev_index_x * smoothing_factor + \
                    index_x * (1 - smoothing_factor)
                smoothed_y = prev_index_y * smoothing_factor + \
                    index_y * (1 - smoothing_factor)

                prev_index_x, prev_index_y = smoothed_x, smoothed_y

                # Move the mouse to the smoothed index finger position
                pyautogui.moveTo(smoothed_x, smoothed_y)

                # Draw circles at index and thumb tips
                cv2.circle(frame, (int(index_finger_tip.x * frame_width),
                           int(index_finger_tip.y * frame_height)), 10, (0, 255, 255), -1)
                cv2.circle(frame, (int(thumb_tip.x * frame_width),
                           int(thumb_tip.y * frame_height)), 10, (255, 0, 255), -1)

                # 📌 Click Detection (Thumb + Index)
                distance = np.hypot(thumb_x - index_x, thumb_y - index_y)
                if distance < 50:
                    current_time = cv2.getTickCount() / cv2.getTickFrequency()
                    if current_time - prev_click_time < 0.5:  # Double Click
                        pyautogui.doubleClick()
                        cv2.putText(frame, "Double Click", (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        pyautogui.click()
                        cv2.putText(frame, "Click", (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    prev_click_time = current_time  # Update last click time

                # 📌 Scroll Detection (Middle Finger Up/Down)
                if middle_y < screen_height // 3:
                    pyautogui.scroll(5)  # Scroll up
                    cv2.putText(frame, "Scrolling Up", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                elif middle_y > 2 * screen_height // 3:
                    pyautogui.scroll(-5)  # Scroll down
                    cv2.putText(frame, "Scrolling Down", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Display the video feed
        cv2.imshow('Virtual Mouse', frame)

        # Exit on pressing 'ESC'
        if cv2.waitKey(1) & 0xFF == 27:
            tracking = False

    cap.release()
    cv2.destroyAllWindows()


def stop_camera():
    """Stops the camera tracking."""
    global tracking
    tracking = False


def ui_interface():
    """Launches the PyWebview frontend with custom styling."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hand Tracking Virtual Mouse</title>
        <style>
            body { text-align: center;
                   font-family: Arial, sans-serif;
                   padding: 50px;
                   background-color: #282c34;
                   color: white;
                  }
                  
            button { padding: 15px 30px;
                     font-size: 18px;
                     margin: 10px;
                     cursor: pointer;
                     border: none;
                     border-radius: 5px;
                    }

            .start { background-color: #4CAF50;
                     color: white;
                    }
                    
                    
            .stop { background-color: #f44336;
                    color: white; 
                   }

            h1 { font-size: 24px; }

        </style>
        <script>
            function startCamera() {
                window.pywebview.api.start_tracking();
            }
            function stopCamera() {
                window.pywebview.api.stop_tracking();
            }
        </script>
    </head>
    <body>
        <h1>Hand Tracking Virtual Mouse</h1>
        <button class="start" onclick="startCamera()">Start Camera</button>
        <button class="stop" onclick="stopCamera()">Stop Camera</button>
    </body>
    </html>
    """
    return html


class API:
    def start_tracking(self):
        """Starts the tracking in a new thread."""
        threading.Thread(target=start_camera, daemon=True).start()

    def stop_tracking(self):
        """Stops the tracking."""
        stop_camera()


if __name__ == "__main__":
    api = API()
    webview.create_window("Hand Tracking", html=ui_interface(), js_api=api)
    webview.start()
>>>>>>> 9fb01e4 (Initial commit)
