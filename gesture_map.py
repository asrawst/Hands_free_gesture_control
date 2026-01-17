
from pynput.keyboard import Controller, Key

keyboard = Controller()

# Mapping MediaPipe default gestures to actions
GUI_GESTURES = {
    "Closed_Fist": lambda: print("Action: Fist (e.g., Grab/Hold)"),
    "Open_Palm": lambda: print("Action: Open Palm (e.g., Stop/Release)"),
    "Thumb_Up": lambda: print("Action: Thumbs Up (e.g., Approve)"),
    "Thumb_Down": lambda: print("Action: Thumbs Down (e.g., Disapprove)"),
    "Pointing_Up": lambda: print("Action: Pointing Up (e.g., Scroll Up)"),
    "Victory": lambda: print("Action: Victory (e.g., Peace)"),
    "ILoveYou": lambda: print("Action: I Love You")
}

def execute_action(gesture_name):
    action = GUI_GESTURES.get(gesture_name)
    if action:
        action()
    elif gesture_name != "None":
        print(f"Unknown gesture: {gesture_name}")
