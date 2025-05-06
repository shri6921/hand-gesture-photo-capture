import cv2
import mediapipe as mp
import time
import os
import tkinter as tk
from threading import Thread
from datetime import datetime
from PIL import Image, ImageTk

class HandPhotoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Photo Capture")
        self.root.geometry("800x600")

        # Initialize OpenCV and MediaPipe
        self.cap = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        # State variables
        self.running = False
        self.two_fingers_detected = False
        self.countdown_start = None
        self.photo_taken = False

        # GUI elements
        self.label_status = tk.Label(root, text="Press Start to begin", font=("Arial", 14))
        self.label_status.pack(pady=10)

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack(pady=10)

        self.btn_start_stop = tk.Button(root, text="Start", font=("Arial", 12), command=self.toggle_start_stop)
        self.btn_start_stop.pack(pady=10)

        # Save directory
        self.save_dir = "captured_photos"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        # Update GUI
        self.update_gui()

    def toggle_start_stop(self):
        if not self.running:
            self.running = True
            self.btn_start_stop.config(text="Stop")
            self.label_status.config(text="Camera starting...")
            self.cap = cv2.VideoCapture(0)
            Thread(target=self.process_video, daemon=True).start()
        else:
            self.running = False
            self.btn_start_stop.config(text="Start")
            self.label_status.config(text="Camera stopped")
            if self.cap:
                self.cap.release()
                self.cap = None
            self.canvas.delete("all")

    def process_video(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process hand detection
            results = self.hands.process(frame_rgb)
            self.two_fingers_detected = False

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Count extended fingers
                    finger_tips = [8, 12, 16, 20]  # Index, middle, ring, pinky
                    thumb_tip = 4
                    extended_fingers = 0
                    hand_pos = hand_landmarks.landmark[0].x  # Wrist x-coordinate

                    # Check thumb based on hand orientation
                    thumb_extended = False
                    if hand_pos < 0.5:  # Right hand (on left side of frame)
                        if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[2].x:
                            thumb_extended = True
                    else:  # Left hand
                        if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[2].x:
                            thumb_extended = True

                    # Count extended fingers (excluding thumb)
                    for tip in finger_tips:
                        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                            extended_fingers += 1

                    if extended_fingers == 2 and not thumb_extended:
                        self.two_fingers_detected = True

                    # Draw landmarks
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # Handle countdown and photo capture
            if self.two_fingers_detected and not self.countdown_start and not self.photo_taken:
                self.countdown_start = time.time()
                self.label_status.config(text="Two fingers detected! Capturing in 5 seconds...")

            if self.countdown_start:
                elapsed = time.time() - self.countdown_start
                remaining = 5 - elapsed
                if remaining > 0:
                    self.label_status.config(text=f"Capturing in {int(remaining) + 1} seconds...")
                else:
                    # Capture and save photo
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    photo_path = os.path.join(self.save_dir, f"photo_{timestamp}.jpg")
                    cv2.imwrite(photo_path, cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
                    self.label_status.config(text=f"Photo saved as {photo_path}")
                    self.countdown_start = None
                    self.photo_taken = True

            # Reset photo_taken when fingers are no longer detected
            if not self.two_fingers_detected and self.photo_taken:
                self.photo_taken = False

            # Display frame on canvas
            img = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.canvas.image = img

            # Small delay to prevent GUI freeze
            time.sleep(0.03)

        # Cleanup
        if self.cap:
            self.cap.release()
            self.running = False
            self.btn_start_stop.config(text="Start")
            self.label_status.config(text="Camera stopped")

    def update_gui(self):
        self.root.after(100, self.update_gui)

    def __del__(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = HandPhotoApp(root)
    root.mainloop()