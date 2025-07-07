# # Volume_Control.py
# import cv2
# import numpy as np
# import math
# import HandeTrackingModule as htm
# import platform

# # Platform-specific volume control
# if platform.system() == "Windows":
#     from ctypes import cast, POINTER
#     from comtypes import CLSCTX_ALL
#     from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#     devices = AudioUtilities.GetSpeakers()
#     interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#     volume = cast(interface, POINTER(IAudioEndpointVolume))
#     volMin, volMax = volume.GetVolumeRange()[:2]
# else:
#     # Dummy class to prevent crash on Linux (Render)
#     class DummyVolume:
#         def SetMasterVolumeLevel(self, vol, _): pass
#         def GetVolumeRange(self): return (0, 100)

#     volume = DummyVolume()
#     volMin, volMax = volume.GetVolumeRange()[:2]

# # Initialize hand detector
# detector = htm.HandTDection(detectionCon=0.7)

# def process_frame(img):
#     volBar = 400
#     volPercent = 0

#     img = detector.findHands(img)
#     lmList = detector.findPosition(img, draw=False)

#     if len(lmList) != 0:
#         x1, y1 = lmList[4][1], lmList[4][2]
#         x2, y2 = lmList[8][1], lmList[8][2]
#         cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

#         cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#         cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
#         cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
#         cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

#         length = math.hypot(x2 - x1, y2 - y1)
#         vol = np.interp(length, [50, 300], [volMin, volMax])
#         volBar = np.interp(length, [50, 300], [400, 150])
#         volPercent = np.interp(length, [50, 300], [0, 100])
#         volume.SetMasterVolumeLevel(vol, None)

#         if length < 50:
#             cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

#     cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
#     cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
#     cv2.putText(img, f'Volume: {int(volPercent)}%', (40, 430),
#                 cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

#     return img


# Volume_Control.py
import cv2
import numpy as np
import math
import HandeTrackingModule as htm

# Initialize model
detector = htm.HandTDection(detectionCon=0.7)

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
        volBar = np.interp(length, [50, 300], [400, 150])
        volPercent = np.interp(length, [50, 300], [0, 100])

        # ❌ No actual volume control on cloud
        # volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Display volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'Volume: {int(volPercent)}%', (40, 430),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    return img

