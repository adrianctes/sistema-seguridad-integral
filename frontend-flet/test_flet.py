import flet as ft


def main(page: ft.Page):
    page.title = "Prueba Flet"
    page.add(
        ft.Text("Flet funciona correctamente")
    )


ft.run(main)