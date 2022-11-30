import cv2 as cv
import mediapipe as mp
import math

video=cv.VideoCapture(0,cv.CAP_DSHOW)
#video = cv.VideoCapture('polichinelos.mp4')
pose=mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)
draw = mp.solutions.drawing_utils
contador = 0
check = True

while True:
    success, img = video.read()
    videoRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = Pose.process(videoRGB)
    points = results.pose_landmarks
    draw.draw_landmarks(img, points, pose.POSE_CONNECTIONS)
    h, w, _ = img.shape

    if points:
        peDY = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y * h)
        peDX = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x * w)
        peEY = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y * h)
        peEX = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x * w)
        moDY = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y * h)
        moDX = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].x * w)
        moEY = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y * h)
        moEX = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].x * w)

        distMO = math.hypot(moDX - moEX, moDY - moEY)
        distPE = math.hypot(peDX - peEX, peDY - peEY)
        print(f'maos {distMO} pes {distPE}')
        # maos <=150 pes >=150

        if check == True and distMO <= 150 and distPE >= 150:
            contador += 1
            check = False
        if distMO >150 and distPE <150:
           check = True
        texto = f'QTD {contador}'
        cv.rectangle(img, (20, 240), (280, 120), (255, 0, 0), -1)
        cv.putText(img, texto, (40, 200),cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
    key=cv.waitKey(1)
    if key==27:#Se apertou o ESC
        break
    cv.imshow('Resultado', img)