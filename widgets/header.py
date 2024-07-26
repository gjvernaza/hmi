import flet as ft


def Header():
    return ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        controls=[
            ft.Image(
                src="assets/logo_mecatronica.jpg",
                width=140,
                height=140,
            ),
            ft.Text(
                value="UNIVERSIDAD DE LAS FUERZAS ARMADAS ESPE-L\n Proyecto de Titulación\n Robot Movil Autónomo con Visión Artificial\n",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD,
                size=20,
            ),
            ft.Image(
                src="assets/logo_espe.jpg",
                width=140,
                height=140,
            )
        ]

    )
