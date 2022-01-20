import cv2
import mediapipe as mp
#import glob

classifier = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("LBPHclassifierV3.yml")

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpHolistic = mp.solutions.holistic
holistic = mpHolistic.Holistic()
mpDraw = mp.solutions.drawing_utils
cx = {}
cy = {}
px = {}
py = {}
lista = []

camera = cv2.VideoCapture(3)

def bigger(a, b, c = 0):
    if a > b:
        if a > c:
            return a
        else:
            return c
    elif b > a:
        if b > c:
            return b
        else:
            return c
    elif a == b or a == c:
        return a
    else:
        return b

def smaller(a,b,c = 0):
    if a < b:
        if c == 0:
            return a
        else:
            if a < c:
                return a
            else:
                return c
    elif b < a:
        if c == 0:
            return b
        else:
            if b < c:
                return b
            else:
                return c
    elif a == b or a == c:
        return a
    else:
        return b

def body_detection():
    if resultsp.pose_landmarks:
        lista.clear()
        lista.append(resultsp.pose_landmarks)
        print(lista)
        for Poselms in lista:
            for id, lm in enumerate(Poselms.landmark):
                h, w, c = video.shape
                px[id], py[id] = int(lm.x * w), int(lm.y * h)

            #mpDraw.draw_landmarks(video, resultsp.pose_landmarks, mpHolistic.POSE_CONNECTIONS)
            '''0 a 10 são os pontos no rosto 
               11 e 12 superior torso
               13(centro) e 15 braço direito
               14(centro) e 16 braço esquerdo
               23 e 24 inferior torso
               25(centro joelho) e 27 perna direita
               26(centro joelho) e 28 perna esquerda
               29 31(ponta do pé) direito
               30 32(ponta do pé) esquerdo'''
            # cv2.circle(video, (px[32], py[32]), 5, (255, 0, 0), cv2.FILLED)
            # Torso
            x1 = bigger(px[11], px[12])
            y1 = smaller(py[11], py[12])
            x2 = smaller(px[11], px[12])
            y2 = bigger(py[23], py[24])
            # cv2.rectangle(video, (px[12], py[12]), (px[11], py[23]), (255,0,0), 2)
            cv2.rectangle(video, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(video, "Torso", (x2 - 10, y2 + 30), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

            # Braços Eq / Dir
            x1 = bigger(px[12], px[14], px[16])
            y1 = smaller(py[12], py[14], py[16])
            x2 = smaller(px[12], px[14], px[16])
            y2 = bigger(py[12], py[14], py[16])
            cv2.rectangle(video, (x1, y1 - 10), (x2, y2 + 10), (100, 0, 170), 2)
            cv2.putText(video, "Arm", (x2 - 10, y2 + 30), cv2.FONT_ITALIC, 1, (100, 0, 170), 2)

            x1 = bigger(px[11], px[13], px[15])
            y1 = smaller(py[11], py[13], py[15])
            x2 = smaller(px[11], px[13], px[15])
            y2 = bigger(py[11], py[13], py[15])
            cv2.rectangle(video, (x1, y1 - 10), (x2, y2 + 10), (100, 0, 170), 2)
            cv2.putText(video, "Arm", (x1 - 40, y2 + 30), cv2.FONT_ITALIC, 1, (100, 0, 170), 2)

            # Pernas Eq / Dir
            x1 = bigger(px[24], px[26], px[28])
            y1 = smaller(py[24], py[26], py[28])
            x2 = smaller(px[24], px[26], px[28])
            y2 = bigger(py[24], py[26], py[28])
            cv2.rectangle(video, (x1 + 10, y1 - 10), (x2 - 10, y2 + 10), (0, 0, 255), 2)
            cv2.putText(video, "Leg", (x2 - 10, y2 + 30), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

            x1 = bigger(px[23], px[25], px[27])
            y1 = smaller(py[23], py[25], py[27])
            x2 = smaller(px[23], px[25], px[27])
            y2 = bigger(py[23], py[25], py[27])
            cv2.rectangle(video, (x1 + 10, y1 - 10), (x2 - 10, y2 + 10), (0, 0, 255), 2)
            cv2.putText(video, "Leg", (x1 - 40, y2 + 30), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

            # Pés
            x1 = bigger(px[29], px[31])
            y1 = smaller(py[29], py[31])
            x2 = smaller(px[29], px[31])
            y2 = bigger(py[29], py[31])
            cv2.rectangle(video, (x1 + 10, y1 - 10), (x2 - 10, y2 + 10), (255, 100, 0), 2)
            cv2.putText(video, "Foot", (x2 - 10, y2 + 30), cv2.FONT_ITALIC, 1, (255, 100, 0), 2)

            x1 = bigger(px[30], px[32])
            y1 = smaller(py[30], py[32])
            x2 = smaller(px[30], px[32])
            y2 = bigger(py[30], py[32])
            cv2.rectangle(video, (x1 + 10, y1 - 10), (x2 - 10, y2 + 10), (255, 100, 0), 2)
            cv2.putText(video, "Foot", (x2 - 40, y2 + 30), cv2.FONT_ITALIC, 1, (255, 100, 0), 2)

def face_detection():
    for (x, y, l, a) in faces:
        faceImage = cv2.resize(gray_image[y:y + a, x:x + l], (100, 100))
        cv2.rectangle(video, (x, y), (x + l, y + a), (255, 0, 0), 2)
        id, predict = recognizer.predict(faceImage)
        color = 0, 255, 0

        if id == 1 and predict > 65:
            nome = "Caique"
        else:
            nome = "Desconhecido"
            color = 0, 0, 255

        cv2.putText(video, nome + "-" + str(predict)[0:2:1], (x, y + (a + 30)), cv2.FONT_ITALIC, 0.7, (color))
        print(f"{id}" + "/" + f"{predict}")

def hand_detection():
    if resultsh.multi_hand_landmarks:
        for handLms in resultsh.multi_hand_landmarks:
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
                # 12 dedo do meio, 20 dedinho, 4 dedão, 0 base da mão
                # if id == 4 or id == 12:
            #mpDraw.draw_landmarks(video, handLms, mpHands.HAND_CONNECTIONS)
            # print(f"x={higherx} / y={highery}, cx4={cx[4]}, cx12={cx[12]}")
            cv2.rectangle(video, (lowerx - 20, lowery - 20), (higherx + 20, highery), (0, 255, 0), 2)
            cv2.putText(video, "Hand", (lowerx - 20, highery + 30), cv2.FONT_ITALIC, 1, (0, 255, 0), 2)


while True:
    conection, video = camera.read()
    gray_image = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

    imgRGB = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
    resultsh = hands.process(imgRGB)
    resultsp = holistic.process(imgRGB)

    face_detection()
    hand_detection()
    body_detection()

    cv2.imshow("Face recognizer and body detection", video)
    if cv2.waitKey(2) == ord("q"):
        break
cv2.destroyAllWindows()

