# Hand Tracking Virtual Mouse

This project implements a **Hand Tracking Virtual Mouse** using **OpenCV**, **Mediapipe**, and **Pyautogui**. It allows users to control their mouse using hand gestures, including cursor movement, clicking, and scrolling. The project also features a **PyWebview-based UI** for starting and stopping the camera.

## 🎯 Features
- **Hand Tracking using Mediapipe**: Detects hand landmarks and tracks finger movements.
- **Virtual Mouse Control**:
  - Moves the cursor using the index finger tip.
  - Clicks when the thumb and index finger touch.
  - Detects double-clicks.
- **Scrolling Mechanism**:
  - Scroll up when the middle finger is raised above a threshold.
  - Scroll down when the middle finger is lowered.
- **Smooth Cursor Movement**: Implements a smoothing algorithm to prevent jittery movement.
- **Web Interface for Control**: Uses PyWebview to provide a UI with "Start Camera" and "Stop Camera" buttons.

## 🛠️ Installation
### 1️⃣ Prerequisites
Ensure you have Python installed (>=3.7) and install the required dependencies:
```bash
pip install opencv-python mediapipe pyautogui numpy pywebview
```

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/hand-tracking-mouse.git
cd hand-tracking-mouse
```

### 3️⃣ Run the Script
```bash
python hand_tracking_mouse.py
```

## 🎮 How It Works
1. **Hand Landmark Detection**:
   - Uses **Mediapipe Hands** to detect the positions of fingers.
   - Tracks **index finger tip (8)**, **thumb tip (4)**, and **middle finger tip (12)**.
2. **Mouse Movement**:
   - Moves the cursor based on the index finger’s position.
   - Uses **smoothing** to prevent unstable movement.
3. **Click Detection**:
   - If the **thumb and index finger** come close (<50 pixels), a **click event** is triggered.
   - If clicked twice within **0.5 seconds**, it registers a **double-click**.
4. **Scrolling Detection**:
   - Raises the **middle finger** to scroll **up**.
   - Lowers the **middle finger** to scroll **down**.
5. **Web UI Control**:
   - Click **"Start Camera"** to begin hand tracking.
   - Click **"Stop Camera"** to end tracking.

## 🚀 Future Enhancements
✅ Implement gesture-based **right-click** and **drag & drop**
✅ Add **custom gesture recognition** for shortcuts
✅ Improve **gesture stability** with Kalman Filters
✅ Use **face detection** to prevent unintended movements

## 🙌 Credits
Developed by **Ankit Kumar**.

---
Happy coding! 🚀

