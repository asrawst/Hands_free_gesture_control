# Gesture Control Mouse

A computer vision-based project that allows you to control your mouse cursor using hand gestures via your webcam. Built with Python, OpenCV, and MediaPipe.

## Features

- **Hands-Free Control**: Move the cursor with your index finger.
- **Clicking**: Single pinch (Thumb + Index) to click (opens links).
- **Opening Files**: Double pinch (Thumb + Index) to double-click.
- **Scrolling**: Slide your open palm up or down.
- **Safety**: Triple pinch to instantly quit the application.
- **Visual Feedback**: On-screen annotations for gestures and active zones.

## Prerequisites

- Python 3.8 or higher
- A webcam
- MacOS (optimized for Apple Silicon) / Windows / Linux

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gesture-control.git
   cd gesture-control
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This project requires `opencv-python`, `mediapipe`, `pyautogui`, and `numpy`.*

## Usage

1. **Run the Application**
   ```bash
   python main.py
   ```

2. **Gestures Guide**

   | Action | Gesture | Description |
   | :--- | :--- | :--- |
   | **Move Cursor** | **Index Finger Up** | Lift only your index finger. Move it within the magenta box to reach all screen corners. |
   | **Single Click** | **Single Pinch** | Pinch Thumb & Index finger **once**. Useful for clicking links or buttons. |
   | **Double Click** | **Double Pinch** | Pinch Thumb & Index finger **twice rapidly**. Useful for opening files/folders. |
   | **Scroll** | **Open Palm** | Lift **all 4 fingers**. Slide hand Up to scroll UP, Down to scroll DOWN. |
   | **Quit App** | **Triple Pinch** | Pinch Thumb & Index finger **3 times rapidly**. Exits the program immediately. |

   > **Tip**: Keep your hand about 1-2 feet away from the camera for best detection.

## Configuration

You can adjust sensitivity settings in `main.py`:
- `frame_reduction`: Controls the size of the active tracking box (higher = less hand movement needed).
- `click_cooldown`: Time between clicks to prevent accidental spamming.

## Troubleshooting

- **Permissions**: Ensure your terminal/IDE has permission to access the Camera and control the Mouse (Accessibility settings on Mac).
- **Lighting**: Ensure your hand is well-lit for MediaPipe to track landmarks accurately.
