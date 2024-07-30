import cv2
from time import sleep
#cap = cv2.VideoCapture("http://192.168.0.101/1600x1200.jpg")
cap = cv2.VideoCapture(1)
# Establece la resolución deseada
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    #cap.open("http://192.168.0.101/640x480.jpg")
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    if not ret:
        print("Error al abrir la cámara")
        break
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        # Obtiene las dimensiones de la cámara
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Resolución de la cámara: {frame_width} x {frame_height}")
    