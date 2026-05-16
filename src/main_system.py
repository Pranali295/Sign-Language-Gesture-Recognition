import os
import logging
import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import pyttsx3
import time
from collections import deque, Counter

# -----------------------------
# Suppress warnings
# -----------------------------
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('absl').setLevel(logging.ERROR)

# -----------------------------
# Voice Engine
# -----------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -----------------------------
# Load ML model
# -----------------------------
model = tf.keras.models.load_model("mnist_model.h5", compile=False)
labels = list("ABCDEFGHIKLMNOPQRSTUVWXY")

# -----------------------------
# MediaPipe setup
# -----------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# -----------------------------
# Sentence + timing
# -----------------------------
sentence = ""
last_output = ""
last_time = time.time()

# -----------------------------
# Prediction smoothing
# -----------------------------
pred_history = deque(maxlen=10)

def get_smooth_prediction(pred_list):
    if len(pred_list) == 0:
        return ""
    return Counter(pred_list).most_common(1)[0][0]

# -----------------------------
# Finger detection
# -----------------------------
def get_finger_states(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    states = []

    states.append(hand_landmarks.landmark[4].x <
                  hand_landmarks.landmark[3].x)

    for i in tips[1:]:
        states.append(hand_landmarks.landmark[i].y <
                      hand_landmarks.landmark[i-2].y)

    return states

def distance(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# -----------------------------
# Gesture detection
# -----------------------------
def detect_custom_gesture(hand_landmarks):
    states = get_finger_states(hand_landmarks)

    thumb = hand_landmarks.landmark[4]
    index = hand_landmarks.landmark[8]

    if states == [True, False, False, False, False]:
        return "Thumbs Up 👍"

    if states == [False, True, True, False, False]:
        return "Victory ✌️"

    if states == [True, True, True, True, True]:
        return "Palm ✋"

    if states == [False, False, False, False, False]:
        return "Fist ✊"

    if states == [False, True, False, False, False]:
        return "Index ☝️"

    if states == [True, True, False, False, True]:
        return "Love You 🤟"

    if distance(thumb, index) < 0.05:
        return "OK 👌"

    if distance(thumb, index) < 0.07:
        return "Pinch 🤏"

    if states == [False, True, True, True, True]:
        return "Thank You 🙏"

    return "Unknown"

# -----------------------------
# Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    h, w, _ = frame.shape

    # Right panel
    panel_width = 350
    panel = np.zeros((h, panel_width, 3), dtype=np.uint8)

    alphabet = "Detecting..."
    gesture = "Detecting..."
    confidence = 0.0
    status = "No Hand"

    if results.multi_hand_landmarks:
        status = "Active"

        for hand_landmarks in results.multi_hand_landmarks:

            x_list = [lm.x for lm in hand_landmarks.landmark]
            y_list = [lm.y for lm in hand_landmarks.landmark]

            x_min = int(min(x_list) * w)
            y_min = int(min(y_list) * h)
            x_max = int(max(x_list) * w)
            y_max = int(max(y_list) * h)

            hand_img = frame[y_min:y_max, x_min:x_max]

            # Gesture detection
            gesture = detect_custom_gesture(hand_landmarks)

            # Alphabet detection
            if hand_img.size != 0:
                try:
                    img = cv2.resize(hand_img, (28, 28))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = img / 255.0
                    img = img.reshape(1, 28, 28, 1)

                    pred = model.predict(img, verbose=0)
                    confidence = float(np.max(pred))
                    class_id = np.argmax(pred)

                    if confidence > 0.85:
                        alphabet = labels[class_id]
                        pred_history.append(alphabet)
                    else:
                        alphabet = "Low confidence"

                except:
                    alphabet = "Error"

            # -----------------------------
            # Smooth prediction
            # -----------------------------
            smooth_alpha = get_smooth_prediction(pred_history)

            # -----------------------------
            # Sentence + Voice logic
            # -----------------------------
            current_time = time.time()

            if current_time - last_time > 2:
                output = smooth_alpha if len(smooth_alpha) == 1 else gesture

                if output != last_output and output not in ["Unknown", "Low confidence", ""]:
                    sentence += output + " "
                    speak(output)
                    last_output = output

                last_time = current_time

            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # -----------------------------
    # UI PANEL DESIGN
    # -----------------------------
    cv2.rectangle(panel, (0, 0), (panel_width, h), (40, 40, 40), -1)

    cv2.putText(panel, "AI HAND RECOGNITION", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.line(panel, (10, 60), (panel_width - 10, 60), (100, 100, 100), 1)

    cv2.putText(panel, f"Alphabet: {alphabet}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.putText(panel, f"Gesture: {gesture}", (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(panel, f"Confidence: {confidence:.2f}", (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.putText(panel, f"Status: {status}", (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Sentence display
    cv2.putText(panel, "Sentence:", (20, 270),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.putText(panel, sentence[-30:], (20, 310),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.line(panel, (10, 340), (panel_width - 10, 340), (100, 100, 100), 1)

    cv2.putText(panel, "Controls:", (20, 380),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.putText(panel, "C - Clear", (20, 410),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.putText(panel, "Q - Quit", (20, 440),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # Combine frames
    combined = np.hstack((frame, panel))
    cv2.imshow("Final Year Project 🚀", combined)

    key = cv2.waitKey(1)

    if key == ord('c'):
        sentence = ""

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()