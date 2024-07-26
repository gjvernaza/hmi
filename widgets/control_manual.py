import flet as ft
import socket


def ControlManual(socket: socket.socket):

    def send_data(data: str):
        data = data + "\n"
        try:
            socket.sendall(data.encode())
        except Exception as e:
            print(f"Error al enviar datos: {e}")

    return ft.Container(
        width=200,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/arrow-izq-up.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("0.15,-0.15,0"),
                        ),
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/arrow-up.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("0.25,0,0"),
                        ),
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/arrow-der-up.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("0.15,0.15,0"),
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/arrow-izq.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("0,-0.25,0"),
                        ),
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/stop.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("0,0,0"),
                        ),
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/arrow-der.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("0,0.25,0"),
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/arrow-izq-down.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("-0.15,-0.15,0"),
                        ),
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/arrow-down.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("-0.25,0,0"),
                        ),
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/arrow-der-down.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("-0.15,0.15,0"),
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/rotate-ccw.png",
                                width=40,
                                height=40,
                            ),
                            on_click=lambda e: send_data("0,0,1.5"),
                        ),
                        ft.TextButton(
                            content=ft.Image(
                                src="assets/rotate-cw.png",
                                width=40,
                                height=40,

                            ),
                            on_click=lambda e: send_data("0,0,-1.5"),
                        ),
                    ],
                ),
            ]
        )
    )


