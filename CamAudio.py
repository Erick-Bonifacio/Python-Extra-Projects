import cv2 #Biblioteca de visão computacional, vai auxiliar na captura do video do pc
import math #Usado pra calcular o tamanho da linha entre os dedos
import numpy as np 
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Tamanho da câmera
wCam, hCam = 640, 480

# Inicializar a câmera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Obter o controlador de volume padrão
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Inicializar o módulo de mediapipe para rastreamento de mãos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

while True:
    # Capturar o quadro da câmera
    success, img = cap.read()

    # Converter para RGB (mediapipe utiliza RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detectar mãos
    results = hands.process(img_rgb)

    # Verificar se pelo menos uma mão foi detectada
    if results.multi_hand_landmarks:
        # Obter a posição da ponta do dedo indicador
        hand_landmarks = results.multi_hand_landmarks[0]
        x1, y1 = int(hand_landmarks.landmark[8].x * wCam), int(hand_landmarks.landmark[8].y * hCam)

        # Obter a posição da ponta do dedo polegar
        x2, y2 = int(hand_landmarks.landmark[4].x * wCam), int(hand_landmarks.landmark[4].y * hCam)

        # Desenhar uma linha entre os dedos indicador e polegar
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Calcular a distância entre os dedos indicador e polegar
        length = math.hypot(x2 - x1, y2 - y1)

        # Mapear a distância para o intervalo de volume desejado (0 a 100)
        volume_range = int(np.interp(length, [50, 300], [0, 100]))

        # Definir o volume do sistema
        volume.SetMasterVolumeLevelScalar(volume_range / 100, None)

    # Exibir o resultado
    cv2.imshow("Hand Tracking", img)

    # Sair do loop quando a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
