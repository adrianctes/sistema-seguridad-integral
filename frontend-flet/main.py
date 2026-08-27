import os

import flet as ft
import platform
from components.layout import Layout


def main(page: ft.Page):
    page.padding = 20
    page.window_maximized = True
    
    page.title = "Sistema Integral Seguridad"

    page.theme_mode = ft.ThemeMode.LIGHT

    page.padding = 0

    page.spacing = 0

    page.bgcolor = "#F1F5F9"
    
    # Detectar plataforma
    sistema = platform.system()
    platform_info = {
    "Windows": "Windows Desktop",
    "Darwin": "macOS Desktop",
    "Linux": "Linux Desktop"
}.get(sistema, f"{sistema or 'Movil'}")
    

    layout = Layout(page)

    page.layout = layout
    page.add(layout.build() )
  

    layout.change_view("dashboard")

    page.update()


if __name__ == "__main__":
    ft.run(main) 



