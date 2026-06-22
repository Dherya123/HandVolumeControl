# Hand Gesture Volume Control

Control your computer's volume using hand gestures.

This project uses OpenCV and MediaPipe to track hand landmarks in real time through a webcam. The distance between specific fingers is used to determine the desired volume level, allowing users to increase or decrease system volume without touching the keyboard or mouse.

## 🚀 Features

- Real-time hand tracking
- Hand landmark detection using MediaPipe
- Gesture-based volume adjustment
- Visual feedback for finger distance and volume level
- Smooth and touch-free interaction

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- AppleScript (macOS Volume Control)
- subprocess

## 📸 How It Works

1. Webcam captures live video.
2. MediaPipe detects hand landmarks.
3. The distance between the thumb and index finger is calculated.
4. Finger distance is mapped to the system volume range.
5. Volume is adjusted accordingly.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Dherya123/HandVolumeControl.git
cd HandVolumeControl
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the project

```bash
python VolumeControl.py
```