# Hand Gesture Recognition System

An AI-based real-time Hand Gesture Recognition System developed using MediaPipe, TensorFlow, Keras, and OpenCV.

This project detects and recognizes hand gestures through a webcam using Computer Vision and Deep Learning techniques.

---

# Features

- Real-time hand gesture detection
- Hand landmark tracking using MediaPipe
- Deep Learning based gesture recognition
- Multiple gesture support
- MNIST dataset integration
- CSV dataset generation
- Logging system
- User authentication support
- Real-time webcam interaction

---

# Technologies Used

- Python
- TensorFlow
- Keras
- OpenCV
- MediaPipe
- NumPy
- Pandas

---

# Project Structure

```bash
HAND_GESTURE_RECOGNITION/
│
├── dataset/
├── data/
│   ├── gesture_data.csv
│   ├── sign_mnist_train.csv
│   └── sign_mnist_test.csv
│
├── models/
│   ├── gesture_model.h5
│   ├── mnist_model.h5
│   └── labels.npy
│
├── logs/
│   ├── backup_logs.txt
│   ├── gesture_log.txt
│   └── log.txt
│
├── screenshots/
│
├── config/
│   └── users.json
│
├── src/
│   ├── alphabet_model.py
│   ├── app.py
│   ├── create_csv.py
│   ├── dataset_collection.py
│   ├── gesture_rules.py
│   ├── hand_gesture_ml.py
│   ├── hash_generator.py
│   ├── main_system.py
│   ├── test_hash.py
│   ├── train_mnist_model.py
│   └── train_model.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/hand-gesture-recognition-system.git
```

## Navigate to Project Folder

```bash
cd hand-gesture-recognition-system
```

## Install Required Libraries

```bash
pip install -r requirements.txt
```

---

# Run the Project

```bash
python src/app.py
```

OR

```bash
python src/main_system.py
```

---

# Requirements

- Python 3.10 or above
- Webcam access
- Required Python libraries installed

---

# Screenshots

Add your project screenshots inside the `screenshots/` folder.

Example:

- Real-time gesture detection
- Hand landmark tracking
- Prediction output
- System interface

---

# Future Enhancements

- Voice output integration
- Sentence generation using gestures
- More gesture classes
- Mobile application integration
- Improved model accuracy

---

# Note

This project may require additional setup depending on system configuration, Python version, and installed dependencies.

---

# Author

Pranali Mahankal  
Artificial Intelligence & Data Science Student

---

# License

This project is licensed under the MIT License.
