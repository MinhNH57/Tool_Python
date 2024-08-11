import cv2 
import time
import hand as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

pTime = 0 
cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
volumeComputer  = volume.GetVolumeRange()
minVol = volumeComputer[0]
maxVol = volumeComputer[1]

while True :
    ret , frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame , draw=False)

    if len(lmList) != 0 :
        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2 , y2 = lmList[8][1] , lmList[8][2]

        cv2.circle(frame , (x1 , y1) , 15 , (255 , 0 , 255),-1)
        cv2.circle(frame , (x2 , y2) , 15 , (255 , 0 , 255),-1)
        cv2.line(frame , (x1 , y1) , (x2 , y2),(255 , 0 , 255),3)

        cx,cy = ((x1 + x2) // 2 , (y1+y2)//2) 
        cv2.circle(frame , (cx , cy) , 15 , (255 , 0 , 255),-1)

        length = math.hypot(x2 - x1 , y2 - y1 )
        print("Độ dài :" , length)

        vol = np.interp(length , [5 , 200] , [minVol , maxVol])
        volBar = np.interp(length , [5 , 386] , [400 , 150])
        volume.SetMasterVolumeLevel(vol, None)
        if(length < 25 ):
            cv2.circle(frame , (cx , cy) , 15 , (0 , 255 , 0),-1)

        cv2.rectangle(frame , (50 , 150) , (100 , 400) , (0,255,255),3)
        cv2.rectangle(frame , (50 , int(volBar)) , (100 , 400) , (0,255,255),-1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame , f"FPS : {int(fps)}" , (150 , 70) , cv2.FONT_HERSHEY_COMPLEX , 3 , (255 , 0 , 0) , 3)

    cv2.imshow("Nguyen Hong Minh" , frame)

    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
