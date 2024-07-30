import flet as ft
import base64
import cv2
import numpy as np

#url_camera = "http://192.168.1.2:4747/video"
url_camera = 1
# Cargar diccionario y parámetros de Aruco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
aruco_params = cv2.aruco.DetectorParameters()

# Cargar datos de calibración
calibration_data = np.load("calibration_data.npz")
marker_size = 0.15  # Tamaño del marcador en metros
clicked_points = []  # Lista para almacenar los puntos clicados


class Camera(ft.UserControl):

    def __init__(self, cap=cv2.VideoCapture(url_camera)):
        super().__init__()
        self.cap = cap
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.image = None
        self.image_base64 = None
        self.width = 640
        self.height = 480

    def did_mount(self):
        self.update_timer()

    def pose_estimation(self, frame, mtx, dist):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        x_m = 0.86
        y_m = 0.86
        marker_point = np.array([[x_m, y_m, 0]], dtype=np.float32)
        corners, ids, rejected = cv2.aruco.detectMarkers(
            gray, aruco_dict, parameters=aruco_params)

        if ids is not None:
            for i in range(len(ids)):
                rvects, tvects, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners=corners[i], markerLength=marker_size, cameraMatrix=mtx, distCoeffs=dist)
                cv2.aruco.drawDetectedMarkers(frame, corners)
                cv2.drawFrameAxes(frame, mtx, dist, rvects,
                                  tvects, marker_size)
                image_point, _ = cv2.projectPoints(
                    marker_point, rvects, tvects, mtx, dist)
                image_point = tuple(image_point.ravel().astype(int))
                cv2.circle(frame, image_point, 2, (255, 0, 255), -1)
                cv2.putText(frame, f"({x_m},{y_m})", image_point,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

    def update_timer(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                self.pose_estimation(
                    frame, calibration_data["mtx"], calibration_data["dist"])
                _, buffer = cv2.imencode('.jpg', frame)
                self.image_base64 = base64.b64encode(buffer).decode('utf-8')
                self.img.src_base64 = self.image_base64
                self.update()
            else:
                print("Error al leer la cámara")

    def build(self):
        self.img = ft.Image(
            src_base64="",
            width=self.width,
            height=self.height,
            border_radius=ft.border_radius.all(20)
        )
        return self.img
