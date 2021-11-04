import cv2
import mediapipe as mp
import time

camera = cv2.VideoCapture(3)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
cx = {}
cy = {}
cz = {}

def bigger(a, b, c=0, d=0):
    if a >= b:
        if a >= c and a >= d:
            return a
        elif c >= d:
            return c
        else:
            return d
    elif b >= a:
        if b >= c and b >= d:
            return b
        elif c >= d:
            return c
        else:
            return d


def smaller(a, b, c=0, d=0):
    if c == 0 and d == 0:
        if a <= b:
            return a
        else:
            return b
    elif c == 0:
        if a <= b:
            if a <= d:
                return a
            else:
                return d
        else:
            if b <= d:
                return b
            else:
                return d
    elif d == 0:
        if a <= b:
            if a <= c:
                return a
            else:
                return c
        else:
            if b <= c:
                return b
            else:
                return c
    else:
        if a <= b:
            if a <= c and a <= d:
                return a
            elif c <= d:
                return c
            else:
                return d
        elif b <= a:
            if b <= c and b <= d:
                return b
            elif c <= d:
                return c
            else:
                return d

while True:
    returnCode, video = camera.read()
    imgRGB = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
    #faz a detecção das mãos
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        print(results.multi_hand_landmarks)
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = video.shape
                cx[id], cy[id] = int(lm.x*w), int(lm.y*h)
                if id == 0:
                    lowerx = cx[id]
                    lowery = cy[id]
                    higherx = cx[id]
                    highery = cy[id]
                elif cx[id] < lowerx or cy[id] < lowery or cx[id] > higherx or cy[id] > highery:
                    if cx[id] < lowerx:
                        lowerx = cx[id]
                    if cy[id] < lowery:
                        lowery = cy[id]
                    if cx[id] > higherx:
                        higherx = cx[id]
                    if cy[id] > highery:
                        highery = cy[id]
                #12 dedo do meio, 20 dedinho, 4 dedão, 0 base da mão
                #if id == 4 or id == 12:
            '''x1 = smaller(cx[0], cx[4], cx[12], cx[20])
            x2 = bigger(cx[0], cx[4], cx[12], cx[20])
            y1 = smaller(cx[0], cx[4], cx[12], cx[20])
            y2 = bigger(cx[0], cx[4], cx[12], cx[20])'''
            #cv2.circle(video, (cx[12], cy[12]), 15, (255, 0, 0), cv2.FILLED)
            mpDraw.draw_landmarks(video, handLms, mpHands.HAND_CONNECTIONS)
            #print(f"x={higherx} / y={highery}, cx4={cx[4]}, cx12={cx[12]}")
            cv2.rectangle(video, (lowerx - 20, lowery - 20), (higherx + 20, highery), (255, 0, 0), 2)
            cv2.putText(video, "Hand", (lowerx - 20, highery + 30), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)
    cv2.imshow("Hand Tracking", video)
    cv2.waitKey(1)

camera.release()
cv2.destroyAllWindows()

