import cv2
import mediapipe as mp
from time import sleep
import numpy as np
import pickle
import os.path

class Pessoa:
    def __init__(self, nome, idade, plano, rosto):
        self.__nome = nome
        self.__idade = idade
        self.__plano = plano
        self.__rosto = rosto

    @property
    def nome(self):
        return self.__nome
    
    def getRosto(self):
        return self.__rosto

webcam = cv2.VideoCapture(0)
reconhecimento_rosto = mp.solutions.face_detection
desenho = mp.solutions.drawing_utils
reconhecedor_rosto = reconhecimento_rosto.FaceDetection()
sleep(1)

listaClientes = []

print('Bem-vindo ao reconhecimento facial!\n')

op = int(input("Digite 1 para cadastrar rosto e 2 para ler rosto: "))

while op != 0:
    if op == 1:
        
        input("Pressione Enter para capturar uma imagem...")
        validacao, frame = webcam.read()
        if not validacao:
            print('Erro ao capturar imagem.\n')

        imagem = frame
        lista_rostos = reconhecedor_rosto.process(imagem)

        if lista_rostos.detections:
            for rosto in lista_rostos.detections:
                desenho.draw_detection(imagem, rosto)

        cv2.imshow("Rostos na sua webcam", imagem)

        pessoa = Pessoa("Erick", 18, 'plus', imagem)
        listaClientes.append(pessoa)
        

        print('Imagem lida. Pressione qualquer tecla para fechar a janela.')
        cv2.waitKey(0)  # Espera até que uma tecla seja pressionada
        cv2.destroyAllWindows()
        webcam.release()  # Libera os recursos da webcam
        op = int(input("Digite 1 para cadastrar rosto e 2 para ler rosto: "))

    elif op == 2:
        webcam = cv2.VideoCapture(0)
        while webcam.isOpened():
            validacao, frame = webcam.read() 
            if not validacao:
                break
            imagem = frame
            lista_reconhecer = reconhecedor_rosto.process(imagem) 
            
            if lista_reconhecer.detections:
                for rosto in lista_reconhecer.detections:
                    desenho.draw_detection(imagem, rosto)
                    for cliente in listaClientes:
                        if rosto == cliente.getRosto():
                            print('Acesso liberado!')

            cv2.imshow("Rostos na sua webcam", imagem)
            if cv2.waitKey(5) == 27:
                break

webcam.release()
cv2.destroyAllWindows()
