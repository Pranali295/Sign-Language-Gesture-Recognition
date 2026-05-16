import os
import logging
from datetime import datetime
import time

import cv2
import mediapipe as mp

# -----------------------------
# Suppress warnings
# -----------------------------
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('absl').setLevel(logging.ERROR)

# -----------------------------
# MediaPipe Setup
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# Control Variables
# -----------------------------
current_label = "A"
is_saving = True
last_save_time = 0
save_interval = 0.1

print("Controls:")
print("A-Z → Change Label")
print("SPACE → Pause/Resume Saving")
print("ESC → Quit")

# -----------------------------
# Start Camera
# -----------------------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # -----------------------------
    # Display label & status
    # -----------------------------
    cv2.putText(frame, f"Label: {current_label}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    status_text = "Saving: ON" if is_saving else "Saving: PAUSED"
    cv2.putText(frame, status_text, (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # -----------------------------
    # Auto Save Logic
    # -----------------------------
    current_time = time.time()

    if is_saving and results.multi_hand_landmarks and (current_time - last_save_time > save_interval):
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmarks (63 values)
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            # Save file
            os.makedirs("dataset", exist_ok=True)
            filename = f"dataset/{current_label}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.txt"

            with open(filename, "w") as f:
                f.write(",".join(map(str, landmarks)))

            print(f"Saved: {filename}")

            last_save_time = current_time

    # -----------------------------
    # Show Window
    # -----------------------------
    cv2.imshow("FAST Dataset Collection", frame)

    # -----------------------------
    # Key Controls
    # -----------------------------
    key = cv2.waitKey(1) & 0xFF

    # Change label (A-Z or a-z)
    if (65 <= key <= 90) or (97 <= key <= 122):
        current_label = chr(key).upper()
        print(f"Label changed to: {current_label}")

    # Pause / Resume (SPACE key)
    elif key == 32:
        is_saving = not is_saving
        print("Saving Paused" if not is_saving else "Saving Resumed")

    # Quit (ESC key)
    elif key == 27:
        break

# -----------------------------
# Release Camera
# -----------------------------
cap.release()
cv2.destroyAllWindows()