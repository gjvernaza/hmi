import flet as ft
import socket
import threading

from services.camera import Camera
from widgets.control_autonomo import ControlAutonomo
from widgets.control_manual import ControlManual
from widgets.header import Header


def main(page: ft.Page):
    def radiogroup_changed(event):
        value = event.control.value
        if value == "manual":
            control_manual.disabled = False
            control_manual.opacity = 1.0
            control_autonomo.disabled = True
            control_autonomo.opacity = 0.5
        elif value == "auto":
            control_autonomo.disabled = False
            control_autonomo.opacity = 1.0
            control_manual.disabled = True
            control_manual.opacity = 0.5
        page.update()

    def open_camera(event):
        value = event.control.value
        if value:
            camera.visible = True
            camera.update()
        else:
            camera.visible = False
            camera.update()

    def connect_socket(socket: socket.socket):        

        try:
            
            socket.connect((HOST, PORT))
            print("Conexión establecida")
        except Exception as e:
            print(f"No se pudo conectar al servidor: {e}")
        
                
        page.update()

    
    # parametros principales de la página
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Robot Móvil"
    page.padding = 0

    radio_group = ft.RadioGroup(
        on_change=radiogroup_changed,
        content=ft.Row(
            controls=[
                ft.Radio(value="manual", label="Manual"),
                ft.Radio(value="auto", label="Autónomo"),
            ]
        )
    )

    HOST = '192.168.4.1'  # Dirección IP del ESP32 configurado como AP
    PORT = 80  # Puerto del servidor ESP32
    # Inicialmente el socket está desactivado
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Crear un hilo para la conexión del socket
    thread = threading.Thread(target=connect_socket(s))
    
    
    control_manual = ControlManual(socket=s)
    control_manual.disabled = True
    control_manual.opacity = 0.5

    control_autonomo = ControlAutonomo(s=s, page=page)
    control_autonomo.disabled = True
    control_autonomo.opacity = 0.5

    camera = Camera()
    camera.visible = False

    activate_camera = ft.Switch(
        value=False,
        label="Activar cámara",
        mouse_cursor=ft.MouseCursor.CLICK,
        on_change=open_camera
    )
    
    page.add(
        ft.Column(
            controls=[
                Header(),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    
                                    ft.Text(
                                        value="Modo de Operación", size=15, weight=ft.FontWeight.BOLD),
                                    radio_group,
                                    control_manual,
                                    control_autonomo,
                                ],
                            ),
                        ),
                        ft.Column(
                            controls=[
                                activate_camera,
                                camera,
                            ]
                        ),
                    ]
                )
            ]
        ),
    )
    page.update()
    thread.start()


ft.app(main, name="My App")
