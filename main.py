import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


### CAmera Access Module
cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plot = LivePlot(640, 480, [20, 37], invert=True)

id_list = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
count = 0
while True:

    ret, frame = cap.read()
    frame, faces = detector.findFaceMesh(frame, draw= False)
    if faces:
        face = faces[0]
        for id in id_list:
            cv2.circle(frame, face[id], 5, (0,255,0), cv2.FILLED)
        leftUp = face[159]
        leftDown = face[23]
        left_left = face[130]
        left_right = face[243]
        vert_length, _ = detector.findDistance(leftUp, leftDown)
        hoz_length, _ = detector.findDistance(left_left, left_right)

        cv2.line(frame, leftUp, leftDown, (200, 0, 22), 3)
        cv2.line(frame, left_left, left_right, (200, 0, 22), 3)

        ratio = int((vert_length / hoz_length)*100)
        ratioList.append(ratio)
        if len(ratioList) > 5:
            ratioList.pop(0)
        avgRatio = sum(ratioList) / len(ratioList)

        if avgRatio < 25 and count == 0:
            blinkCounter += 1
            count = 1
        if count != 0:
            count +=1
            if count > 10:
                count = 0
        cvzone.putTextRect(frame, f'Blink Count: {blinkCounter}', (50, 100))
        framePlot = plot.update(avgRatio)

        framestack =  cvzone.stackImages([frame, framePlot], 2 ,1)

    cv2.imshow('Webcame',framestack)
    if cv2.waitKey(20) & 0XFF == ord('q'):
        break
cap.release()