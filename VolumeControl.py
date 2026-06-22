import cv2
import mediapipe as mp
import time
import numpy as np
import math
import osascript
import subprocess

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands, min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)

        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img=frame, center=(cx, cy), radius=15, color=(255, 0, 255), thickness=-1)

        return lmList    

def main():
    cap = cv2.VideoCapture(0)

    prevTime = 0
    currTime = 0
    detector = HandDetector(detectionCon=0.7)

    minVol = 0
    maxVol = 100
    vol = 0
    volBar = 400
    volPer = 0

    while True:
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame, draw=False)

        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 

            cv2.circle(img=frame, center=(x1, y1), radius=15, color=(255, 0, 255), thickness=-1)
            cv2.circle(img=frame, center=(x2, y2), radius=15, color=(255, 0, 255), thickness=-1)
            cv2.line(img=frame, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 255), thickness=3)
            cv2.circle(img=frame, center=(cx, cy), radius=15, color=(255, 0, 255), thickness=-1)

            length = math.hypot(x2 - x1, y2 - y1)

            # Hand Range 50 - 300
            # Volume Range 0 - 100

            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            subprocess.run(["osascript", "-e", f"set volume output volume {vol}"])

        cv2.rectangle(img=frame, pt1=(50, 150), pt2=(85, 400), color=(255, 0, 0), thickness=3)
        cv2.rectangle(img=frame, pt1=(50, int(volBar)), pt2=(85, 400), color=(255, 0, 0), thickness=-1)
        cv2.putText(img=frame, text=f"{int(volPer)} %", org=(40, 450), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_AA)

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        cv2.putText(img=frame, text=f"FPS: {int(fps)}", org=(40, 50), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(255, 0, 0), thickness=3, lineType=cv2.LINE_AA)

        cv2.imshow("Webcam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()