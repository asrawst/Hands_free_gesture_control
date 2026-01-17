
import cv2
import pyautogui
import time
import math
import numpy as np
import util
from vision_engine import VisionEngine

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("cannot open camera")
        exit()

    vision_engine = VisionEngine()
    
    # gesture time control
    click_start_time = None
    click_times = []
    click_cooldown = 0.5
    scroll_mode = False
    freeze_cursor = False
    
    screen_w, screen_h = pyautogui.size()
    print("\n hand mouse control .")
    prev_screen_x, prev_screen_y = 0, 0


    while True:
        ret, frame = cap.read()
        if not ret:
            print("can't receive frame")
            break

        # Flip the frame
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Process frame
        processed_frame, gesture_name, hand_landmarks = vision_engine.process_frame(frame)

        if hand_landmarks:
            # get finger tip (matching screenshot logic)
            # landmarks are accessible via hand_landmarks[i] directly in the protobuf/object
            thumb_tip = hand_landmarks[4]
            index_tip = hand_landmarks[8]
            middle_tip = hand_landmarks[12]
            ring_tip = hand_landmarks[16]
            pinky_tip = hand_landmarks[20]

            # Logic: Check which fingers are up
            # Tips IDs: Index=8, Middle=12, Ring=16, Pinky=20
            # Condition: Tip y < PIP y (since y increases downwards)
            # using landmark object which has .y attribute
            
            # Note: landmarks is a list of objects with x, y, z
            fingers = [
                1 if hand_landmarks[tip].y < hand_landmarks[tip-2].y else 0
                for tip in [8, 12, 16, 20]
            ]

            # distance btwn thumb and index
            dist = math.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
            # Threshold for pinch (Quit/Freeze/Click)
            if dist < 0.05:
                if not freeze_cursor:
                    freeze_cursor = True
                    click_times.append(time.time())
                    # Single Pinch = Click (as requested)
                    pyautogui.click()
                    cv2.putText(processed_frame, "Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Check for 3 Pinches to Quit
                # Increased window to 1.5s to comfortably fit 3 pinches
                if len(click_times) >= 3 and click_times[-1] - click_times[-3] < 1.5:
                    print("Triple pinch detected. Quitting...")
                    break
                # Check for 2 Pinches to Open (Double Click)
                elif len(click_times) >= 2 and click_times[-1] - click_times[-2] < 1.0:
                    pyautogui.doubleClick()
                    cv2.putText(processed_frame, "Open (Double Click)", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            else:
                freeze_cursor = False

            
            # Thumb logic creates a 5th element usually, but screenshot showed loop for 4 tips
            # If we need thumb (tip 4), it's usually checked against x depending on hand side
            
            # For now, just printing to verify logic as implied by screenshot progress
            # print(f"Fingers up: {fingers}") 

            # --- Mouse Control Logic ---
            
            # 1. Moving Mode: Only Index Finger Up
            if fingers[0] == 1 and fingers[1] == 0:
                # Convert coordinates with frame reduction (makes it faster/more sensitive)
                frame_reduction = 100 # Frame Reduction
                cv2.rectangle(processed_frame, (frame_reduction, frame_reduction), (w - frame_reduction, h - frame_reduction),
                (255, 0, 255), 2)
                
                x3 = np.interp(index_tip.x * w, (frame_reduction, w - frame_reduction), (0, screen_w))
                y3 = np.interp(index_tip.y * h, (frame_reduction, h - frame_reduction), (0, screen_h))
                
                # Smoothen values (reduced factor from 5 to 2 for less lag/more speed)
                curr_screen_x = prev_screen_x + (x3 - prev_screen_x) / 2
                curr_screen_y = prev_screen_y + (y3 - prev_screen_y) / 2
                
                # Move Mouse
                pyautogui.moveTo(curr_screen_x, curr_screen_y)
                prev_screen_x, prev_screen_y = curr_screen_x, curr_screen_y
                
            # 2. Clicking Mode: Both Index and Middle Fingers Up
            if fingers[0] == 1 and fingers[1] == 1:
                # Find distance between fingers (Visual feedback only now, click logic assumes just UP)
                # But we'll verify distance to avoid accidental clicks if hands are just relaxed open?
                # User request: "to select file middle finger and index finger up"
                # Removed the length < 40 check. Just being UP triggers click.
                
                lm_list = [
                    (index_tip.x * w, index_tip.y * h),
                    (middle_tip.x * w, middle_tip.y * h)
                ]
                length = util.get_distance(lm_list)
                
                # If both up, we click.
                # Use cooldown to prevent spamming
                if length < 1000: # Always true basically, just keeping structure
                    cv2.circle(processed_frame, (int(lm_list[0][0]), int(lm_list[0][1])), 15, (0, 255, 0), cv2.FILLED)
                    
                    # Simple cooldown check
                    current_time = time.time()
                    if click_start_time is None or (current_time - click_start_time) > click_cooldown:
                         pyautogui.click()
                         click_start_time = current_time
                         print("Click!")
                         print("Click!")
                         cv2.putText(processed_frame, "Click!", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 3. Scrolling Mode: All 4 Fingers Up (Open Palm)
            if fingers == [1, 1, 1, 1]:
                 # Reuse mapping logic for consistency
                frame_reduction = 100
                x3 = np.interp(index_tip.x * w, (frame_reduction, w - frame_reduction), (0, screen_w))
                y3 = np.interp(index_tip.y * h, (frame_reduction, h - frame_reduction), (0, screen_h))
                
                # Smoothen
                curr_screen_x = prev_screen_x + (x3 - prev_screen_x) / 2
                curr_screen_y = prev_screen_y + (y3 - prev_screen_y) / 2
                
                # Calculate movement delta
                # Screen Y increases downwards.
                # Hand Up -> y3 decreases -> delta negative -> Scroll Up
                # Hand Down -> y3 increases -> delta positive -> Scroll Down
                delta_y = curr_screen_y - prev_screen_y
                
                # Threshold to avoid jitter
                if abs(delta_y) > 5:
                    # Scroll magnitude
                    # pyautogui.scroll(amount): + is up, - is down on some OS, check?
                    # On Mac: scroll UP is + values (content moves down).
                    # User said "Palm slide up to scroll up".
                    # Hand moving up (delta < 0). We want to scroll up (which usually means content moves down -> PAGE UP equivalent).
                    # Actually "Scroll up" usually means seeing content above, so wheel turns up.
                    # pyautogui.scroll(10) -> Scrolls up.
                    # So if delta_y < -5 (Hand moving up), scroll(10).
                    
                    scroll_amount = int(delta_y / 1.5) # Scaling factor (Reduced speed: added /1.5)
                    # Invert because moving hand UP (negative delta) should scroll UP (positive value)?
                    # Or natural scrolling?
                    # Let's try direct mapping first: Hand Up -> Scroll Up.
                    # Delta negative -> Scroll positive.
                    pyautogui.scroll(-scroll_amount) 
                    
                    cv2.putText(processed_frame, "Scrolling...", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                
                # Update prev coords so we track continuous movement
                prev_screen_x, prev_screen_y = curr_screen_x, curr_screen_y

        cv2.imshow("live video", processed_frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

