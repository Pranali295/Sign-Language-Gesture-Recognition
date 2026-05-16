import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# -----------------------------
# Load & Clean CSV Data
# -----------------------------
data = []
labels = []

with open("gesture_data.csv", "r") as f:
    for line in f:
        values = line.strip().split(",")

        if len(values) != 64:
            continue

        # ✅ Remove quotes
        clean_values = [v.replace('"', '') for v in values[:-1]]

        data.append(list(map(float, clean_values)))
        labels.append(values[-1])

X = np.array(data)
y = np.array(labels)

print("Total samples:", len(X))

# -----------------------------
# Encode Labels
# -----------------------------
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Save labels
np.save("labels.npy", encoder.classes_)

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# -----------------------------
# Build Model
# -----------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(63,)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(len(encoder.classes_), activation='softmax')
])

# -----------------------------
# Compile
# -----------------------------
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# -----------------------------
# Train
# -----------------------------
model.fit(X_train, y_train, epochs=20, batch_size=32)

# -----------------------------
# Evaluate
# -----------------------------
loss, acc = model.evaluate(X_test, y_test)
print("Accuracy:", acc)

# -----------------------------
# Save Model
# -----------------------------
model.save("gesture_model.h5")

print("Model saved successfully!")