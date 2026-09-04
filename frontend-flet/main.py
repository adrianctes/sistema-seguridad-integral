import os

import flet as ft
import platform
from components.layout import Layout
from views.login.login_view import LoginView

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

    def mostrar_login(): 
        login = LoginView( 
            page=page, 
            on_login=mostrar_legajos )
        page.controls.clear() 
        page.add(login.build())
        page.update()
    
    def mostrar_legajos():
        layout = Layout(
            page,
            on_logout=mostrar_login
        )

        page.layout = layout
        page.controls.clear()
        page.add(layout.build())
        layout.change_view("legajos")
        page.update()
    
    """ page.layout = layout
    page.add(layout.build() )
  

    layout.change_view("dashboard") """

    #page.update()
    mostrar_login()

if __name__ == "__main__":
    ft.run(main) 



