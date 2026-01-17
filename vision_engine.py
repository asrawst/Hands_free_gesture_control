
import cv2
import mediapipe as mp
import time
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class VisionEngine:
    def __init__(self):
        try:
            base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
            options = vision.GestureRecognizerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.VIDEO,
                num_hands=1,
                min_hand_detection_confidence=0.7,
                min_hand_presence_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.recognizer = vision.GestureRecognizer.create_from_options(options)
            self.start_time = time.time()
        except Exception as e:
            print(f"Failed to initialize GestureRecognizer: {e}")
            self.recognizer = None

    def process_frame(self, frame):
        if not self.recognizer:
            return frame, None

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        # Calculate timestamp in ms
        timestamp_ms = int((time.time() - self.start_time) * 1000)
        
        # Recognize
        result = self.recognizer.recognize_for_video(mp_image, timestamp_ms)
        
        gesture_name = None
        hand_landmarks_proto = None
        
        if result.gestures:
             # Get top gesture
            top_gesture = result.gestures[0][0]
            gesture_name = top_gesture.category_name
            
            # Get landmarks for the first hand
            if result.hand_landmarks:
                hand_landmarks_proto = result.hand_landmarks[0]
                
            # Draw landmarks manually since solutions.drawing_utils might be missing
            self._draw_landmarks(frame, result.hand_landmarks)

            # Display gesture name on screen
            cv2.putText(frame, f"Gesture: {gesture_name}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return frame, gesture_name, hand_landmarks_proto

    def _draw_landmarks(self, frame, hand_landmarks_list):
        if not hand_landmarks_list:
            return
            
        h, w, _ = frame.shape
        for landmarks in hand_landmarks_list:
            # Convert normalized landmarks to pixel coordinates
            points = []
            for lm in landmarks:
                x, y = int(lm.x * w), int(lm.y * h)
                points.append((x, y))
                # Draw red landmarks (BGR: 0, 0, 255)
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            
            # Calculate and draw center crosshair
            if points:
                # Simple centroid
                center_x = int(sum(p[0] for p in points) / len(points))
                center_y = int(sum(p[1] for p in points) / len(points))
                
                # Draw black crosshair
                cv2.line(frame, (center_x - 10, center_y), (center_x + 10, center_y), (0, 0, 0), 2)
                cv2.line(frame, (center_x, center_y - 10), (center_x, center_y + 10), (0, 0, 0), 2)

            # Draw connections (White lines: 255, 255, 255)
            # Palm
            self._draw_line(frame, points[0], points[1])
            self._draw_line(frame, points[1], points[5])
            self._draw_line(frame, points[5], points[9])
            self._draw_line(frame, points[9], points[13])
            self._draw_line(frame, points[13], points[17])
            self._draw_line(frame, points[17], points[0])
            
            # Fingers
            for i in range(0, 4): self._draw_line(frame, points[1+i], points[2+i]) # Thumb
            for i in range(0, 3): self._draw_line(frame, points[5+i], points[6+i]) # Index
            for i in range(0, 3): self._draw_line(frame, points[9+i], points[10+i]) # Middle
            for i in range(0, 3): self._draw_line(frame, points[13+i], points[14+i]) # Ring
            for i in range(0, 3): self._draw_line(frame, points[17+i], points[18+i]) # Pinky

    def _draw_line(self, frame, p1, p2):
        cv2.line(frame, p1, p2, (255, 255, 255), 2)
