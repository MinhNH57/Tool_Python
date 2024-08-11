import cv2
import time
import os
import hand as htm 

cap=cv2.VideoCapture(0)

FolderPath="./Fingers"
lst=os.listdir(FolderPath)
lst_2=[] 
for i in lst:
    image=cv2.imread(f"{FolderPath}/{i}")  # Fingers/1.jpg , Fingers/2.jpg ...
    lst_2.append(image)
pTime=0

detector =htm.handDetector(detectionCon=0.55)
#0.75 độ chính xác 75%

fingerid= [4,8,12,16,20]
while True:
    ret,frame =cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False) # phát hiện vị trí
    print (lmList)




    if len(lmList) !=0:
        fingers= []
        # viết cho ngón cái (ý tường là điểm 4 ở bên trái hay bên phải điểm 2 )
        if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        print(lmList)
        # viết cho 4 ngón dài
        for id in range(1,5):
            if lmList[fingerid[id]][2] < lmList[fingerid[id]-2][2]:
                fingers.append(1)
                print(lmList[fingerid[id]][2])
                print(lmList[fingerid[id]-2][2])
            else:
                fingers.append(0)


        print(fingers)
        songontay=fingers.count(1)
        print(songontay)


        h, w, c = lst_2[songontay-1].shape
        frame[0:h,0:w] = lst_2[songontay-1] 

        # vẽ thêm hình chữ nhật hiện số ngón tay
        cv2.rectangle(frame,(0,200),(150,400),(0,255,0),-1)
        cv2.putText(frame,str(songontay),(30,390),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),5)

    cTime=time.time()  # trả về số giây, tính từ 0:0:00 ngày 1/1/1970 theo giờ  utc , gọi là(thời điểm bắt đầu thời gian)
    fps=1/(cTime-pTime) # tính fps Frames per second - đây là  chỉ số khung hình trên mỗi giây
    pTime=cTime
    # show fps lên màn hình, fps hiện đang là kiểu float , ktra print(type(fps))
    cv2.putText(frame, f"FPS: {int(fps)}",(150,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)


    cv2.imshow("Ga Lai LAp Trinh",frame)
    if cv2.waitKey(1)== ord("q"): # độ trễ 1/1000s , nếu bấm q sẽ thoát
        break
cap.release() # giải phóng camera
cv2.destroyAllWindows() # thoát tất cả các cửa sổ