import numpy as np
import cv2
import pygame
import random
import os
import time

class DrowsinessDetector:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Initialize video capture (0 for default camera, try 1 if 0 doesn't work)
        self.cap = cv2.VideoCapture(1)
        
        # Load cascade classifiers for face and eye detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
        
        # Initialize variables
        self.count = 0
        self.status = "awake"
        self.message = ""
        self.alarm_playing = False
        
        # Load alarm sound
        script_dir = os.path.dirname(os.path.abspath(__file__))
        alarm_path = os.path.join(script_dir, 'alarm.mp3')
        self.alarm = pygame.mixer.Sound(alarm_path)
        
        # Funny messages for when drowsiness is detected
        self.messages = [
            "Wake up, you idiot!",
            "Hey sleepyhead, eyes on the road!",
            "Stop dreaming and start driving!",
            "Coffee break needed!",
            "Wakey wakey, eggs and bakey!",
            "Snap out of it!",
            "No snoozing allowed!",
            "Are you sleeping on the job?",
            "Alert! Human malfunction detected!",
            "WAKE UP! Life is happening!"
        ]
    
    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, "no_camera"
        
        # Convert to grayscale and apply filter for better detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 5, 1, 1)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # Draw rectangle around the face
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                
                # Detect eyes in the face region
                eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
                
                # Draw rectangles around eyes
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
                
                # Check if both eyes are detected
                if len(eyes) >= 2:
                    cv2.putText(frame, "Eyes open!", (100, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    self.alarm.stop()
                    self.alarm_playing = False
                    self.count = 0
                    self.status = "awake"
                    self.message = "Eyes open!"
                else:
                    # Blink detected, increment counter
                    self.count += 1
                    self.message = f"Blink detected ({self.count}/3)"
                    
                    # If blink persists for 3 frames, consider it drowsiness
                    if self.count >= 3:
                        self.message = random.choice(self.messages)
                        cv2.putText(frame, self.message, (100, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                        
                        if not self.alarm_playing:
                            self.alarm.play(-1)  # Play in loop until stopped
                            self.alarm_playing = True
                        
                        self.status = "drowsy"
                    time.sleep(0.5)  # Slight delay to avoid rapid counting
        else:
            cv2.putText(frame, "No face detected", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
            self.status = "no_face"
            self.message = "No face detected"
        
        return frame, self.status
    
    def get_status(self):
        return self.status
    
    def get_message(self):
        return self.message
    
    def release(self):
        if self.alarm_playing:
            self.alarm.stop()
        self.cap.release()

# For direct testing
if __name__ == "__main__":
    detector = DrowsinessDetector()
    
    while True:
        frame, status = detector.process_frame()
        if frame is not None:
            cv2.imshow('Drowsiness Detection', frame)
            
            # Press 'q' to exit
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break
    
    detector.release()
    cv2.destroyAllWindows()