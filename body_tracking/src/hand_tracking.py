import cv2
import mediapipe as mp

camera = cv2.VideoCapture(3)

##  Importa as ferramentas responsáveis por realizar a detecção das mãos
mpHands = mp.solutions.hands

##  Cria o objeto hand
hands = mpHands.Hands()

##  Importa as ferramentas de desenho, responsáveis por traçar as linhas entre os pontos das mãos
mpDraw = mp.solutions.drawing_utils

##  Dicionários onde serão armazenados os valores da coordenada em pixels de cada ponto das mãos em seus respectivos eixos
cx = {}
cy = {}

while camera.isOpened():
    returnCode, video = camera.read()

    ##  Faz a conversão do tipo de imagem, pois o mediapipe Hands trabalha com imagens do tipo RGB
    imgRGB = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)

    ##  Faz a detecção dos pontos das mãos
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:

        ##  Navega na lista onde estão armazenadas as coordenadas de cada mão detectada
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):

                ##  As coordenadas dos são dadas em decimal, um valor que corresponde a uma proporção da imagem mostrada na tela
                ##  Portanto é necessário obter o tamanho do vídeo (altura e largura) e multiplicar as coordenadas x pela largura e as y pela altura para obter o valor em pixels
                h, w = video.shape[:2]
                cx[id], cy[id] = int(lm.x*w), int(lm.y*h)

            ###################################################################
            #         Obtenção de pontos com maiores e menores valores        #
            #  de cada parte do corpo para melhor representação ao delimitar  #
            ###################################################################

            for i in sorted(cx, key=cx.get):
                lowerx = cx[i]
                break

            for i in sorted(cx, key=cx.get, reverse=True):
                higherx = cx[i]
                break

            for i in sorted(cy, key=cy.get):
                lowery = cy[i]
                break

            for i in sorted(cy, key=cy.get, reverse=True):
                highery = cy[i]
                break

            ''' 12 dedo do meio
                20 dedinho
                4 dedão
                0 base da mão ''' 

            ##  Pode utilizar essa função para desenhar um circulo e testar cada ponto do corpo              
            #cv2.circle(video, (cx[12], cy[12]), 15, (255, 0, 0), cv2.FILLED)

            ##  Função responsável por fazer a ligação dos pontos corporais. Desenha os pontos do corpo, mãos e face, entretanto é necessário passar como parâmetro qual parte deseja (nesse caso, os pontos do corpo)
            mpDraw.draw_landmarks(video, handLms, mpHands.HAND_CONNECTIONS)
            
            cv2.rectangle(video, (lowerx - 20, lowery - 20), (higherx + 20, highery), (255, 0, 0), 2)
            cv2.putText(video, "Hand", (lowerx - 20, highery + 30), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)

    cv2.imshow("Hand Tracking", video)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

