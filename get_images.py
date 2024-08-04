import cv2

from time import sleep

cap = cv2.VideoCapture(1)

# Establece la resolución deseada
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    if not ret:
        print("Error al abrir la cámara")
        break
    ## tomar 15 fotos al aplastar la letra s
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        for i in range(15):
            cv2.imwrite(f"foto{i}.jpg", frame)
            sleep(1)