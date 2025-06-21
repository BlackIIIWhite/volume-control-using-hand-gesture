import cv2
import numpy as np
import HandTracking as htm
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


# To get access of system volume
device = AudioUtilities.GetSpeakers()
interface = device.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = interface.QueryInterface(IAudioEndpointVolume)

minvol = -63.5
maxvol = 0.0
# Set volume to -20.0 dB


# Capture Video from web cam
video = cv2.VideoCapture(0)
# Import module (HandDetector)
detector = htm.HandDetector(min_detection_confidence = 0.7)
while True:
    ret, frame = video.read()
    if ret:
        detector.findHands(frame)

        # Require hand index
        hands = [4, 8, 12]

        listlm = detector.findPosition(frame, hands)
        if listlm:

            # hand co-ordinate
            id1, x1, y1 = listlm[4]
            id2, x2, y2 = listlm[8]
            id3, x3, y3 = listlm[12]


            # line between hand index 4 & 8
            cv2.line(frame, (int(x1), int(y1)),(int(x2), int(y2)),(0, 0, 0),3)

        # to show line between hand index 8 & 12
            # cv2.line(frame, (int(x2), int(y2)), (int(x3), int(y3)), (0, 255, 0), 3)

            # to find length between hand index 8 & 12
            length2 = math.hypot((x3 - x2), (y3 - y2))

            # to stop changing volume if the distance of hand index iis more than 50, so you can stop the changing volume
            if length2 < 50 :

                # to get co-ordinate of x and y to create circle between hand index 4 & 8
                cx = (int(x1)+int(x2))//2
                cy = (int(y1)+int(y2))//2
                cv2.circle(frame, (int(cx), int(cy)), 10, (255,0,0), cv2.FILLED)

                # to find length between hand index 4 & 8
                length = math.hypot((x2-x1), (y2-y1))

                # to Convert the length in the range of (-63.5, 0.0 )
                vol = np.interp(length,[45,250], [-63.5,0.0])

                # For percentage of volume
                volper = np.interp(vol, [-63.5,0.0], [0,100])

                # For volume bar
                volbar = np.interp(vol, [-63.5, 0.0], [190, 110])
                cv2.rectangle(frame,(70,190),(90,110),(0, 0, 0),3)
                cv2.rectangle(frame, (70, 190), (90, int(volbar)), (200, 200, 200), -1)
                cv2.putText(frame, f'Volume {int(volper)}%', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

                # Set the volume
                volume.SetMasterVolumeLevel(vol, None)
                if length <=40:
                    cv2.circle(frame, (int(cx), int(cy)), 10, (0, 255, 0), cv2.FILLED)
        # frame = cv2.flip(frame, 1)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) &0xFF == ord('q'):
            break