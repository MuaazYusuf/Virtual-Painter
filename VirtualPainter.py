import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

brushThickness = 15
eraserThickness = 50

folderPath = "Header"

myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
   image = cv2.imread(f'{folderPath}/{imPath}')
   overlayList.append(image)

header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(min_detection_confidence=0.85)

xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()

    # solve mirror problem
    img = cv2.flip(img, 1)

    # find hand landmarks
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList[0]) != 0 and len(lmList[1]) != 0:
        print(lmList[0][8][1:])
        print(lmList[0][12][1:])
        # tip of index and middle fingers
        x1, y1 = lmList[0][8][1:]
        x2, y2 = lmList[0][12][1:]

    # check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
    # If selection mode - Two fingers are up  > Dont draw
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection Mode")
            if y1 < 129:
                if 130 < x1 < 350:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 450 < x1 < 620:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 750 < x1 < 900:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1150:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25),
                          drawColor, cv2.FILLED)
    # If Drawing mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, eraserThickness)
            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInverse = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInverse = cv2.cvtColor(imgInverse, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInverse)
    img = cv2.bitwise_or(img, imgCanvas)
    # setting the header image
    img[0:129, 0:1170] = header
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.imshow("Image Canvas", imgCanvas)
    cv2.imshow("Invers", imgInverse)
    cv2.waitKey(1)
