import flet as ft
import base64
import cv2
import numpy as np

#url_camera = "http://192.168.1.2:4747/video"
url_camera = 2
# Cargar diccionario y parámetros de Aruco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
aruco_params = cv2.aruco.DetectorParameters()

# Cargar datos de calibración
calibration_data = np.load("calibration_data.npz")
marker_size = 0.145  # Tamaño del marcador en metros
print(calibration_data["mtx"])


class Camera(ft.UserControl):

    def __init__(self, cap=cv2.VideoCapture(url_camera)):
        super().__init__()
        self._cap = cap
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self._image = None
        self._image_base64 = None
        self._width = 640
        self._height = 480        
        # Lista para almacenar las posiciones sucesivas del marcador
        self._marker_positions = []
        # Para almacenar la posición inicial del centro del marcador
        self._initial_marker_center = None
        self._points_x = []
        self._points_y = []
        # Lista para almacenar una vez los puntos de las coordenadas x e y
        self._px = None
        self._py = None
        #self.image_point = [(180,666),(400,846),(1130,420)]
        self.image_point = []
        
        

    def did_mount(self):
        self.update_timer()
    
    def clean_frame(self):
        self._marker_positions.clear()
        self.image_point.clear()
        self._points_x.clear()
        self._points_y.clear()
        self._px = None
        self._py = None
    
    def set_points(self, points_x: list, points_y: list):
        self._points_x = points_x
        self._points_y = points_y

    def pose_estimation(self, frame, mtx, dist):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        
        corners, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

        if ids is not None:
            rvects, tvects, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners=corners, markerLength=marker_size, cameraMatrix=mtx, distCoeffs=dist)
            cv2.aruco.drawDetectedMarkers(frame, corners)
            cv2.drawFrameAxes(frame, mtx, dist, rvects, tvects, marker_size, thickness=5)

            for i in range(len(ids)):
                # Calcular el centro del marcador
                # Promedio de coordenadas x
                center_x = int(np.mean(corners[i][0][:, 0]))
                # Promedio de coordenadas y
                center_y = int(np.mean(corners[i][0][:, 1]))
                self.marker_center = (center_x, center_y)

                # Guardar la posición inicial del centro del marcador si aún no se ha guardado
                if self._initial_marker_center is None:
                    self._initial_marker_center = self.marker_center
                    print(self._initial_marker_center)
                    
                
                # Guardar la posición actual del marcador
                self._marker_positions.append(self.marker_center)

                # Dibujar el punto fijo
                if self._initial_marker_center is not None:
                    cv2.circle(frame, self._initial_marker_center, 5,(0, 0, 255), -1)  # Punto rojo, relleno
                    cv2.putText(frame, "(0,0)", (self._initial_marker_center[0] + 10, self._initial_marker_center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
                    # Dibujar la trayectoria del marcador
                    for j in range(1, len(self._marker_positions)):
                        # Línea verde
                        cv2.line(frame, self._marker_positions[j - 1], self._marker_positions[j], (0, 255, 0), 5)
                
                if len(self._points_x) > 0 and len(self._points_y) > 0:
                    #print("points")
                    if self._px is None and self._py is None:
                        self._px = self._points_x
                        self._py = self._points_y
                        
                        if self._points_x[1] == 1.1:
                            self.image_point = [(210,624),(375, 802),(1173, 301)]
                        elif self._points_x[1] == 2.2:
                            self.image_point = [(210,624),(590,1050),(1390,480)]
                        
                        for x_m, y_m in zip(self._px, self._py):
                          
                            marker_point = np.array([[x_m, y_m, 0]]).astype(np.float32)
                            #point_pixels, _ = cv2.projectPoints(marker_point, rvects, tvects, mtx, dist)
                            #print(point_pixels)
                            #self.image_point.append(tuple(point_pixels.ravel().astype(int)))
                            
                            
                            

                if self._px is not None and self._py is not None:
                    for k in range(len(self.image_point)-1):
                        #cv2.circle(frame, (self.image_point[k]), 10, (0, 255, 0), -1)
                        cv2.line(frame, self.image_point[k], self.image_point[k+1], (0, 0, 255), 4)
                    

    def update_timer(self):
        while True:
            ret, frame = self._cap.read()
            if ret:
                self.pose_estimation(frame, calibration_data["mtx"], calibration_data["dist"])
                _, buffer = cv2.imencode('.jpg', frame)
                self._image_base64 = base64.b64encode(buffer).decode('utf-8')
                self.img.src_base64 = self._image_base64
                self.update()
            else:
                print("Error al leer la cámara")

    def build(self):
        self.img = ft.Image(
            src_base64="",
            width=self._width,
            height=self._height,
            border_radius=ft.border_radius.all(20)
        )
        return self.img
