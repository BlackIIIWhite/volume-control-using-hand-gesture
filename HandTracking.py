import cv2
import numpy as np
import mediapipe as mp


class HandDetector:
    def __init__(self, static_image_mode = False,  model_complexity = 1, smooth_landmarks = True, min_detection_confidence = 0.5, min_tracking_confidence = 0.5):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode, model_complexity, smooth_landmarks, min_detection_confidence, min_tracking_confidence)
        self.mpdraw = mp.solutions.drawing_utils


    def findHands(self, frame):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            return frame

    def findPosition(self,frame, hands=0):
        listlm = []
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for i in hands:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        listlm.append([id, cx, cy])
                        if id == i:
                            cv2.circle(frame, (cx, cy), 10, (0, 0, 0), -1)
                    self.mpdraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
            return listlm


def main():
    detector = HandDetector()
    video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()
        if ret:
            detector.findHands(frame)
            hands= [4, 8, 12]
            listlm = detector.findPosition(frame, hands)
            if listlm:
                print(listlm[4],listlm[12])
            frame = cv2.flip(frame, 1)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    main()


