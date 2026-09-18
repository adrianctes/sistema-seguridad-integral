
import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings


class CambiarPasswordView(ft.Container):

    def __init__(self, page: ft.Page,  on_logout):

        super().__init__()

        self.page_ref = page
        self.on_logout = on_logout

        self.toast = Toast()

        self.expand = True
        self.bgcolor = "#F1F5F9"
        self.padding = 20

        self.usuario_id = 0
        self.username = ""

        # ==========================================================
        # CAMPOS
        # ==========================================================

        self.txt_password_actual = ft.TextField(
            label="Contraseña actual",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            width=450,
            height=55,
            enable_interactive_selection=False,
        )

        self.txt_password_nueva = ft.TextField(
            label="Nueva contraseña",
            prefix_icon=ft.Icons.LOCK_RESET_OUTLINED,
            password=True,
            can_reveal_password=True,
            width=450,
            height=55,
        )

        self.txt_confirmar_password = ft.TextField(
            label="Confirmar nueva contraseña",
            prefix_icon=ft.Icons.LOCK_RESET_OUTLINED,
            password=True,
            can_reveal_password=True,
            width=450,
            height=55,
        )

        # ==========================================================
        # BOTONES
        # ==========================================================

        self.btn_guardar = ft.FilledButton(
            "Cambiar contraseña",
            icon=ft.Icons.LOCK_RESET,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),
                bgcolor="#030B16",
            ),
            on_click=lambda e: self.page_ref.run_task(
                self.cambiar_password
            ),
        )

        self.btn_cancelar = ft.OutlinedButton(
            "Cancelar",
            icon=ft.Icons.ARROW_BACK,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),
            ),
            on_click=self.volver,
        )

        # ==========================================================
        # TITULO
        # ==========================================================

        self.lbl_titulo = ft.Text(
            "Cambiar contraseña",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="#030B16",
        )

        self.lbl_subtitulo = ft.Text(
            "Ingrese la contraseña actual y la nueva contraseña",
            size=14,
            color="#64748B",
        )

        self.lbl_usuario = ft.Text(
            "",
            size=15,
            weight=ft.FontWeight.BOLD,
            color="#334155",
        )

       
        # ==========================================================
        # CONTENIDO
        # ==========================================================

        self.content = self.build()

    # ==============================================================
    # BUILD
    # ==============================================================

    def build(self):

        return ft.Stack(
            expand=True,
            controls=[

                ft.Column(
                    expand=True,
                    spacing=15,
                    controls=[

                        # --------------------------------------------------
                        # HEADER
                        # --------------------------------------------------

                        ft.Container(
                            padding=ft.Padding.only(
                                left=5,
                                right=5,
                                top=5,
                                bottom=5,
                            ),
                            content=ft.Column(
                                spacing=3,
                                controls=[
                                    self.lbl_titulo,
                                    self.lbl_subtitulo,
                                ],
                            ),
                        ),

                        # --------------------------------------------------
                        # FORMULARIO
                        # --------------------------------------------------

                        ft.Container(
                            bgcolor=ft.Colors.WHITE,
                            border=ft.Border.all(
                                1,
                                "#E2E8F0",
                            ),
                            padding=25,
                            expand=True,
                            content=ft.Column(
                                spacing=20,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[

                                    # Usuario
                                    ft.Container(
                                        width=450,
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.PERSON_OUTLINE,
                                                    color="#64748B",
                                                ),
                                                self.lbl_usuario,
                                            ],
                                            spacing=10,
                                        ),
                                    ),

                                    ft.Divider(
                                       
                                        height=1,
                                        color="#E2E8F0",
                                    ),

                                    # Contraseña actual
                                    self.txt_password_actual,

                                    # Nueva contraseña
                                    self.txt_password_nueva,

                                    # Confirmar contraseña
                                    self.txt_confirmar_password,

                                    ft.Container(
                                        width=450,
                                        padding=ft.Padding.only(
                                            top=5,
                                            bottom=5,
                                        ),
                                        content=ft.Text(
                                            "La nueva contraseña debe coincidir "
                                            "con la confirmación.",
                                            size=12,
                                            color="#64748B",
                                        ),
                                    ),

                                    ft.Divider(
                                        height=1,
                                        color="#E2E8F0",
                                    ),

                                    # Botones
                                    ft.Container(
                                        width=450,
                                        content=ft.Row(
                                            alignment=ft.MainAxisAlignment.END,
                                            spacing=10,
                                            controls=[
                                                self.btn_cancelar,
                                                self.btn_guardar,
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),

                self.toast,
            ],
        )

    # ==============================================================
    # SET MODE
    # ==============================================================

    def set_mode(
        self,
        usuario_id: int,
        username: str = "",
    ):

        self.usuario_id = usuario_id
        self.username = username

        self.limpiar_formulario()

        self.lbl_usuario.value = (
            f"Usuario: {username}"
            if username
            else f"Usuario ID: {usuario_id}"
        )


    # ==============================================================
    # LIMPIAR
    # ==============================================================

    def limpiar_formulario(self):

        self.txt_password_actual.value = ""
        self.txt_password_nueva.value = ""
        self.txt_confirmar_password.value = ""

        self.txt_password_actual.error_text = None
        self.txt_password_nueva.error_text = None
        self.txt_confirmar_password.error_text = None

    # ==============================================================
    # VALIDAR
    # ==============================================================

    async def validar(self):

        password_actual = (
            self.txt_password_actual.value or ""
        )

        password_nueva = (
            self.txt_password_nueva.value or ""
        )

        confirmar = (
            self.txt_confirmar_password.value or ""
        )

        # ----------------------------------------------------------
        # Contraseña actual
        # ----------------------------------------------------------

        if not password_actual:

            await self.toast.show(
                self.page_ref,
                "Ingrese la contraseña actual",
                "error",
            )

            self.update()
            return False

        # ----------------------------------------------------------
        # Nueva contraseña
        # ----------------------------------------------------------

        if not password_nueva:
            await self.toast.show(
                self.page_ref,
                "Ingrese la nueva contraseña",
                "error",
            )

            self.update()
            return False

        # ----------------------------------------------------------
        # Confirmación
        # ----------------------------------------------------------

        if not confirmar:

            self.txt_confirmar_password.error_text = (
              
            )
            await self.toast.show(
                    self.page_ref,
                    "Confirme la nueva contraseña",
                    "error",
            )

            self.update()
            return False

        # ----------------------------------------------------------
        # Coincidencia
        # ----------------------------------------------------------

        if password_nueva != confirmar:

            self.txt_confirmar_password.error_text = (
              
            )

            await self.toast.show(
                self.page_ref,
                "Las contraseñas no coinciden",
                "error",
            )

            self.update()
            return False

        # ----------------------------------------------------------
        # No permitir misma contraseña
        # ----------------------------------------------------------

        if password_actual == password_nueva:
            await self.toast.show(
                self.page_ref,
                "La nueva contraseña debe ser diferente",
                "error",
            )
            

            self.update()
            return False

        return True

    # ==============================================================
    # CAMBIAR PASSWORD
    # ==============================================================
    async def cambiar_password(self, e=None):

        # ==========================================================
        # ACTIVAR LOADING
        # ==========================================================

        self.btn_guardar.disabled = True

        self.btn_guardar.content = ft.ProgressRing(
            width=20,
            height=20,
            stroke_width=2,
        )

        self.btn_guardar.icon = None

        self.update()

        try:

            # ======================================================
            # VALIDAR
            # ======================================================

            if not await self.validar():
                return

            # ======================================================
            # TOKEN
            # ======================================================

            token = self.page_ref.session.store.get(
                "access_token"
            )

            if not token:

                await self.toast.show(
                    self.page_ref,
                    "Sesión expirada",
                    "error",
                )

                return

            # ======================================================
            # PAYLOAD
            # ======================================================

            payload = {
                "password_actual": (
                    self.txt_password_actual.value or ""
                ),
                "password_nueva": (
                    self.txt_password_nueva.value or ""
                ),
                "password_confirmacion": (
                    self.txt_confirmar_password.value or ""
                ),
            }

            # ======================================================
            # HEADERS
            # ======================================================

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            # ======================================================
            # URL
            # ======================================================

            url = (
                f"{settings.URL_BACKEND}"
                f"/usuarios/{self.usuario_id}/password"
            )

            print("URL:", url)
            print("USUARIO ID:", self.usuario_id)

            # ======================================================
            # REQUEST
            # ======================================================

            async with httpx.AsyncClient(
                timeout=10
            ) as client:

                response = await client.patch(
                    url,
                    json=payload,
                    headers=headers,
                )

            print(
                "STATUS:",
                response.status_code
            )

            # ======================================================
            # SESIÓN EXPIRADA
            # ======================================================

            if response.status_code == 401:

                await self.toast.show(
                    self.page_ref,
                    "Sesión expirada",
                    "error",
                )

                return

            # ======================================================
            # OK
            # ======================================================

            if response.status_code in (200, 204):

                await self.toast.show(
                    self.page_ref,
                    "Contraseña cambiada correctamente",
                    "success",
                )

                # Volver al login
                self.page_ref.run_task(
                    self.volver_despues_de_guardar
                )

                return

            # ======================================================
            # ERROR BACKEND
            # ======================================================

            try:

                error_data = response.json()

            except Exception:

                error_data = {}

            print(
                "ERROR BACKEND:",
                error_data
            )

            detail = error_data.get(
                "detail",
                "No se pudo cambiar la contraseña",
            )

            # ------------------------------------------------------
            # FastAPI validation error
            # ------------------------------------------------------

            if isinstance(detail, list):

                mensajes = []

                for item in detail:

                    if isinstance(item, dict):

                        mensajes.append(
                            str(
                                item.get(
                                    "msg",
                                    "Error de validación",
                                )
                            )
                        )

                    else:

                        mensajes.append(
                            str(item)
                        )

                if mensajes:
                    detail = " | ".join(mensajes)

            # ======================================================
            # MOSTRAR ERROR
            # ======================================================

            await self.toast.show(
                self.page_ref,
                str(detail),
                "error",
            )

        # ==========================================================
        # TIMEOUT
        # ==========================================================

        except httpx.ConnectTimeout:

            await self.toast.show(
                self.page_ref,
                "No se pudo conectar con el servidor",
                "error",
            )

        # ==========================================================
        # ERROR HTTP
        # ==========================================================

        except httpx.RequestError as ex:

            print(
                f"Error HTTP: {ex}"
            )

            await self.toast.show(
                self.page_ref,
                "Error de conexión con el servidor",
                "error",
            )

        # ==========================================================
        # ERROR GENERAL
        # ==========================================================

        except Exception as ex:

            print(
                f"Error cambiando contraseña: {ex}"
            )

            await self.toast.show(
                self.page_ref,
                "Error cambiando contraseña",
                "error",
            )

        # ==========================================================
        # RESTAURAR BOTÓN
        # ==========================================================

        finally:

            self.btn_guardar.disabled = False

            self.btn_guardar.content = ft.Text(
                "Cambiar contraseña"
            )

            self.btn_guardar.icon = ft.Icons.LOCK_RESET

            self.update()
        
    # ==============================================================
    # VOLVER
    # ==============================================================

    def volver(self, e=None):

        self.page_ref.layout.change_view(
            "gestionar_usuarios"
        )

    # ==============================================================
    # VOLVER DESPUÉS DE GUARDAR
    # ==============================================================

    async def volver_despues_de_guardar(self):

        await self._esperar()

        """ self.page_ref.layout.change_view(
            "gestionar_usuarios"
        )

        # ----------------------------------------------------------
        # Recargar listado
        # ----------------------------------------------------------

        usuarios_view = (
            self.page_ref.layout.views.get(
                 "gestionar_usuarios"
            )
        )

        if usuarios_view:

            self.page_ref.run_task(
                usuarios_view.reload_view
            ) """
         # Limpiar sesión
        self.page_ref.session.store.clear()

        # Volver al login
        self.on_logout()

    # ==============================================================
    # PEQUEÑA ESPERA PARA MOSTRAR TOAST
    # ==============================================================

    async def _esperar(self):

        import asyncio

        await asyncio.sleep(1)

    def bloquear_pegar(self, e):

        # Ctrl + V
        if e.ctrl and e.key.lower() == "v":

            if self.txt_password_actual.focused:
                return