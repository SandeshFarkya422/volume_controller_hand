# import cv2
# import time
# import numpy as np
# import math
# import HandeTrackingModule as htm  # Make sure the spelling is correct
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# # Webcam setup
# wCam, hCam = 640, 480
# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)

# # Hand detector
# detector = htm.HandTDection(detectionCon=0.7)  # Confirm class name spelling in your module

# # Volume control setup
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# volMin, volMax = volume.GetVolumeRange()[:2]

# # Initialize values
# vol = 0
# volBar = 400
# volPercent = 0
# pTime = 0

# while True:
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList = detector.findPosition(img, draw=False)

#     if len(lmList) != 0:
#         # Thumb and index finger tips
#         x1, y1 = lmList[4][1], lmList[4][2]
#         x2, y2 = lmList[8][1], lmList[8][2]
#         cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

#         # Visual elements
#         cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#         cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED) 
#         cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
#         cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

#         # Calculate length and map to volume
#         length = math.hypot(x2 - x1, y2 - y1)
#         vol = np.interp(length, [50, 300], [volMin, volMax])
#         volBar = np.interp(length, [50, 300], [400, 150])
#         volPercent = np.interp(length, [50, 300], [0, 100])

#         # Set system volume
#         volume.SetMasterVolumeLevel(vol, None)

#         # Visual cue when fingers are very close
#         if length < 50:
#             cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

#     # Volume bar
#     cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
#     cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
#     cv2.putText(img, f'Volume: {int(volPercent)}%', (40, 430),
#                 cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

#     # FPS
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (500, 50),
#                 cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

#     cv2.imshow("Volume Hand Control", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# Volume_Control.py
import cv2
import numpy as np
import math
import HandeTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize model & volume
detector = htm.HandTDection(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volMin, volMax = volume.GetVolumeRange()[:2]

def process_frame(img):
    volBar = 400
    volPercent = 0

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [50, 300], [volMin, volMax])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPercent = np.interp(length, [50, 300], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'Volume: {int(volPercent)}%', (40, 430),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    return img
