import numpy as np
import tensorflow as tf

# Load model once
model = tf.keras.models.load_model("gesture_model.h5", compile=False)

labels = np.load("labels.npy")

def predict_alphabet(landmarks):
    if len(landmarks) != 63:
        return "?"

    prediction = model.predict(np.array([landmarks]), verbose=0)
    return labels[np.argmax(prediction)]