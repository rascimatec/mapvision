import cv2
import mediapipe as mp

camera = cv2.VideoCapture('/dev/video2')

##  Importa as ferramentas de desenho, responsáveis por traçar as linhas entre os pontos do corpo
mpDraw = mp.solutions.drawing_utils

##  Importa o holistic model, responsável por fazer o rastreamento corporal
mpHolistic = mp.solutions.holistic

##  Cria o objeto holistic
holistic = mpHolistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

##  Dicionários onde serão armazenados os valores da coordenada em pixels de cada ponto do corpo em seus respectivos eixos
px = {}
py = {}

##  Lista onde serão armazenados todos os resultados de coordenadas obtidos de cada ponto
landmark_list = []


##  Função responsável por retornar o ponto com maior valor na coordenada x ou y
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

##  Função responsável por retornar o ponto com menor valor na coordenada x ou y
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


while camera.isOpened():
    returnCode, video = camera.read()

    ##  Faz a conversão do tipo de imagem, pois o mediapipe Holistic trabalha com imagens RGB
    RGBimage = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)

    ##  Faz a detecção de todos os pontos do corpo
    results = holistic.process(RGBimage)

    ##  O holistic model gera a detecção de pontos do corpo, mãos e face. Como estamos trabalhando somente com detecção corporal, apenas é necessário filtrar os resultados do corpo (pose_landmarks)
    if results.pose_landmarks:
        ##  Armazena os resultados da detecção dos pontos do corpo em uma lista para poder trabalhar com cada ponto individualmente
        landmark_list.clear()
        landmark_list.append(results.pose_landmarks)

        ##  Navega na lista onde estão as coordenadas dos pontos
        for Poselms in list:
            for id, lm in enumerate(Poselms.landmark):

                ##  As coordenadas dos são dadas em decimal, um valor que corresponde a uma proporção da imagem mostrada na tela
                ##  Portanto é necessário obter o tamanho do vídeo (altura e largura) e multiplicar as coordenadas x pela largura e as y pela altura para obter o valor em pixels
                h, w = video.shape[:2]
                px[id], py[id] = int(lm.x * w), int(lm.y * h)        
            
            '''0 a 10 são os pontos no rosto 
               11 e 12 superior torso
               13(centro) e 15 braço direito
               14(centro) e 16 braço esquerdo
               23 e 24 inferior torso
               25(centro joelho) e 27 perna direita
               26(centro joelho) e 28 perna esquerda
               29 31(ponta do pé) direito
               30 32(ponta do pé) esquerdo'''
            
            ###################################################################
            #         Obtenção de pontos com maiores e menores valores        #
            #  de cada parte do corpo para melhor representação ao delimitar  #
            ###################################################################

            # Torso
            x1 = bigger(px[11], px[12], px[23], px[24])
            y1 = smaller(py[11], py[12], py[23], py[24])
            x2 = smaller(px[11], px[12], px[23], px[24])
            y2 = bigger(py[11], py[12], py[23], py[24])            
            cv2.rectangle(video, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(video, "Torso", (x2 - 10, y2 + 30), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

            # Braços Esquerdo / Direito
            x1 = bigger(px[12], px[14], px[16])
            y1 = smaller(py[12], py[14], py[16])
            x2 = smaller(px[12], px[14], px[16])
            y2 = bigger(py[12], py[14], py[16])
            cv2.rectangle(video, (x1 + 10, y1 - 10), (x2 - 10, y2 + 10), (100, 0, 170), 2)
            cv2.putText(video, "Arm", (x2 - 10, y2 + 30), cv2.FONT_ITALIC, 1, (100, 0, 170), 2)

            x1 = bigger(px[11], px[13], px[15])
            y1 = smaller(py[11], py[13], py[15])
            x2 = smaller(px[11], px[13], px[15])
            y2 = bigger(py[11], py[13], py[15])
            cv2.rectangle(video, (x1 + 10, y1 - 10), (x2 - 10, y2 + 10), (100, 0, 170), 2)
            cv2.putText(video, "Arm", (x1 - 40, y2 + 30), cv2.FONT_ITALIC, 1, (100, 0, 170), 2)

            # Pernas Esquerda / Direita
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

            # Pés Direito / Esquerdo
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

            ##  Função responsável por fazer a ligação dos pontos corporais. Desenha os pontos do corpo, mãos e face, entretanto é necessário passar como parâmetro qual parte deseja (nesse caso, os pontos do corpo)
            mpDraw.draw_landmarks(video, results.pose_landmarks, mpHolistic.POSE_CONNECTIONS)

            ##  Pode utilizar essa função para desenhar um circulo e testar cada ponto do corpo
            #cv2.circle(BGRimage, (px[20], py[20]), 5, (255, 0, 0), cv2.FILLED)

    cv2.imshow("Video", video)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
