
# Inicia la captura de video desde la cámara (normalmente 0 es la cámara predeterminada)
##cap = cv2.VideoCapture(0)

import cv2

# Define la función de callback para manejar el evento de clic del ratón


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Muestra las coordenadas en la imagen
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, f'({x},{y})', (x, y), font, 0.5, (255, 0, 0), 2)
        cv2.imshow('Cámara', frame)
        print(f'Coordenadas: ({x}, {y})')


# Inicia la captura de la cámara
cap = cv2.VideoCapture(2)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    # Lee un frame de la cámara
    ret, frame = cap.read()
    cv2.resize(frame, (1920,1080))
    if not ret:
        break

    # Muestra el frame en una ventana
    
    cv2.imshow('Cámara', frame)
    
    
    # Registra la función de callback para la ventana
    cv2.setMouseCallback('Cámara', click_event)

    # Espera la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y destruye las ventanas
cap.release()
cv2.destroyAllWindows()
