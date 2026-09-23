""" import os
import flet as ft
import platform

from components.layout import Layout
from views.login.login_view import LoginView
from views.usuarios.usuario_cambiar_password import CambiarPasswordView

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
    }.get(
        sistema,
        f"{sistema or 'Movil'}"
    )

    def mostrar_cambiar_contrasena():

        cambiar = CambiarPasswordView(
            page=page,
            on_logout=mostrar_login
        )

        usuario = page.session.store.get("usuario")

        if usuario:
            cambiar.set_mode(
                usuario_id=usuario["id"],
                username=f'{usuario["nombre"]} {usuario["apellido"]}'
            )

        page.controls.clear()
        page.add(cambiar)

        page.update()

    def mostrar_login():
        login = LoginView(
            page=page,
            on_login=mostrar_legajos,
            on_change_password=mostrar_cambiar_contrasena
        )

        page.controls.clear()
        page.add(login.build())
        login.limpiar()

        page.update()

   
    
    def mostrar_legajos():
        layout = Layout(
            page,
            on_logout=mostrar_login
        )

        page.layout = layout

        page.controls.clear()
        page.add(layout.build())

        # NO hacer change_view("legajos")
        # Dashboard ya es la vista inicial.

        page.update()

    def on_connect(e):
        mostrar_login()

    page.on_connect = on_connect
    
    mostrar_login()


if __name__ == "__main__":
    ft.run(main) """

import flet as ft
import platform

from components.layout import Layout
from views.login.login_view import LoginView
from views.usuarios.usuario_cambiar_password import CambiarPasswordView


def main(page: ft.Page):

    page.padding = 20
    page.window_maximized = True

    page.title = "Sistema Integral Seguridad"

    page.theme_mode = ft.ThemeMode.LIGHT

    page.padding = 0
    page.spacing = 0
    page.bgcolor = "#F1F5F9"

    # =====================================================
    # DETECTAR PLATAFORMA
    # =====================================================

    sistema = platform.system()

    platform_info = {
        "Windows": "Windows Desktop",
        "Darwin": "macOS Desktop",
        "Linux": "Linux Desktop"
    }.get(
        sistema,
        f"{sistema or 'Movil'}"
    )

    # =====================================================
    # LOGIN
    # =====================================================

    def mostrar_login():

        login = LoginView(
            page=page,
            on_login=mostrar_legajos,
            on_change_password=mostrar_cambiar_contrasena_obligatorio
        )

        page.controls.clear()
        page.add(login.build())

        login.limpiar()

        page.update()

    # =====================================================
    # CAMBIAR CONTRASEÑA NORMAL
    # =====================================================

    def mostrar_cambiar_contrasena():

        cambiar = CambiarPasswordView(
            page=page,
            on_logout=mostrar_login
        )

        usuario = page.session.store.get("usuario")

        if usuario:
            cambiar.set_mode(
                usuario_id=usuario["id"],
                username=f'{usuario["nombre"]} {usuario["apellido"]}'
            )

        page.controls.clear()
        page.add(cambiar)

        page.update()

    # =====================================================
    # CAMBIAR CONTRASEÑA OBLIGATORIO
    # =====================================================

    def mostrar_cambiar_contrasena_obligatorio():

        cambiar = CambiarPasswordView(
            page=page,
            on_logout=mostrar_login,
            on_password_changed=mostrar_legajos
        )

        usuario = page.session.store.get("usuario")

        # =====================================================
        # AGREGAR PRIMERO EL CONTROL A LA PÁGINA
        # =====================================================

        page.controls.clear()
        page.add(cambiar)

        # =====================================================
        # CONFIGURAR DESPUÉS
        # =====================================================

        if usuario:
            cambiar.set_mode(
                usuario_id=usuario["id"],
                username=f'{usuario["nombre"]} {usuario["apellido"]}'
            )

        cambiar.set_modo_obligatorio(True)

        page.update()
    # =====================================================
    # SISTEMA PRINCIPAL
    # =====================================================

    def mostrar_legajos():

        layout = Layout(
            page,
            on_logout=mostrar_login
        )

        page.layout = layout

        page.controls.clear()
        page.add(layout.build())

        # Dashboard es la vista inicial

        page.update()

    # =====================================================
    # CONEXIÓN
    # =====================================================

    def on_connect(e):
        mostrar_login()

    page.on_connect = on_connect

    # =====================================================
    # INICIO
    # =====================================================

    mostrar_login()


if __name__ == "__main__":
    ft.run(main)