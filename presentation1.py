import cv2 as cv
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np
#variáveis
largura, altura = 1280,720
listaSlides = "Presentation"

#slides
pastaSlides = sorted(os.listdir(listaSlides),key=len)
# print(pastaSlides)

#pegando a imagem da webcam
cam = cv.VideoCapture(0)
cam.set(3,largura)
cam.set(4,altura)

#variaveis
imgNumber = 0
altp, largp = int(120*1.2), int(213*1.2)
limitToDetec = 300
buttonPressed = False#ativação
buttonCounter = 0#ponto incial até o delay
buttonDelay = 18#Delay
annotations = [[]]
annotationNumber = -1
annotationStart = False
verif = False
#detector de mãos com coeficiente de  precisão 0.8, e no máximo 1 mão
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    success, img = cam.read()
    img = cv.flip(img,1)
    imageFull = os.path.join(listaSlides,pastaSlides[imgNumber])#conjunto dos slides
    imgAtual = cv.imread(imageFull)#slide da vez

    hands, img = detector.findHands(img)
    #traçando uma linha delimitadora da região onde o algoritmo irá funcionar
    # cv.line(img,(0,limitToDetec),(largura,limitToDetec),(0,0,0),10)

    if hands and buttonPressed is False:
        if len(hands)==2:
            hand = hands[0]      
            fingers = detector.fingersUp(hand)
            cx, cy = hand['center']
            lmList = hand['lmList']
            hand2 = hands[1]      
            fingers2 = detector.fingersUp(hand2)
            cx2, cy2 = hand2['center']
            lmList2 = hand2['lmList']
            print(fingers,fingers2)
        else:
            hand = hands[0]      
            fingers = detector.fingersUp(hand)
            cx, cy = hand['center']
            lmList = hand['lmList']
        #facilitar desenho por toda tela
        #converte um range em outro
        xVal = int(np.interp(lmList[8][0],[380,600],[0,largura]))
        yVal = int(np.interp(lmList[8][1],[150,alt-350],[0,altura]))
        indexFinger = xVal,yVal
        print(fingers)
        if cy <= limitToDetec:
            # gesto 1 - esquerda
            if fingers == [1,0,0,0,0]:
                print("esquerda")               
                if imgNumber > 0:
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
                    buttonPressed = True
                    imgNumber -=1
            # gesto 2 - direita
            if fingers == [0,0,0,0,1]:
                print("direita")               
                if imgNumber < len(pastaSlides) -1:
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
                    buttonPressed = True
                    imgNumber +=1
        #gesto 3 - mostrar ponteiro
        if fingers ==[0,1,0,0,0]:
            cv.circle(imgAtual,indexFinger,8,(0,0,255),cv.FILLED)
         #gesto 4 - desenhar
        if fingers ==[0,1,1,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv.circle(imgAtual,indexFinger,8,(0,0,255),cv.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False
        #gesto 5 - apagar
        if fingers ==[0,1,1,1,1]:
                annotations = [[]]
                annotationNumber = -1
                annotationStart = False
        #gesto 6 - agradecimento
        if len(hands)==2:
            if fingers2 ==[1,1,1,1,1]:
                cv.putText(imgAtual,"Thanks",(250,300),cv.FONT_HERSHEY_SCRIPT_COMPLEX,6,(0,0,0),4)
            if fingers ==[1,1,1,1,1]:
                cv.putText(imgAtual,"for listening!",(150,520),cv.FONT_HERSHEY_SCRIPT_COMPLEX,6,(0,0,0),4)
    #button pressed
    if buttonPressed:
        buttonCounter+=1
        if buttonCounter>=buttonDelay:
            buttonPressed = False
            buttonCounter = 0
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv.line(imgAtual,annotations[i][j-1],annotations[i][j],(0,0,200),8)

    #add imagem da webcam no slide
    imgPequena = cv.resize(img,(largp,altp))
    alt, larg, _ = imgAtual.shape
    imgAtual[0:altp, largura-largp:largura] = imgPequena

    # cv.imshow("Imagem", img)
    cv.imshow("Slides", imgAtual)
    tecla = cv.waitKey(1)
    if tecla == ord('q'):
        break
