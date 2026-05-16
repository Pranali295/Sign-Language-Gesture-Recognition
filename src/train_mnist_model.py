import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv("sign_mnist_train.csv")

print("Dataset loaded:", data.shape)

# Labels
y = data['label'].values

# Features
X = data.drop('label', axis=1).values

# Normalize
X = X / 255.0

# Reshape (important for CNN)
X = X.reshape(-1, 28, 28, 1)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# CNN Model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28,28,1)),

    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(25, activation='softmax')
])

# Compile
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Evaluate
loss, acc = model.evaluate(X_test, y_test)
print("Final Accuracy:", acc)

# Save
model.save("mnist_model.h5")

print("Model saved successfully!")