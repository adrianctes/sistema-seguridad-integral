
import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings


class CrearUsuarioView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page
        self.toast = Toast()

        self.expand = True
        self.bgcolor = "#F1F5F9"
        self.padding = 20

        self.usuario_id = 0
        self.modo_edicion = False

        # ==========================================================
        # CAMPOS
        # ==========================================================

        self.txt_username = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            expand=True,
            height=55,
        )

        self.txt_nombre = ft.TextField(
            label="Nombre",
            prefix_icon=ft.Icons.BADGE_OUTLINED,
            expand=True,
            height=55,
        )

        self.txt_apellido = ft.TextField(
            label="Apellido",
            prefix_icon=ft.Icons.BADGE_OUTLINED,
            expand=True,
            height=55,
        )

        self.cmb_rol = ft.Dropdown(
            label="Rol",
            #icon=ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED,
            expand=True,
            height=55,
            options=[
                ft.DropdownOption(key="SUPERADMINISTRADOR", text="SUPERADMINISTRADOR"),
                ft.DropdownOption(key="ADMINISTRADOR", text="ADMINISTRADOR"),
                ft.DropdownOption(key="OPERADOR", text="OPERADOR"),
                ft.DropdownOption(key="LIQUIDADOR", text="LIQUIDADOR"),
                ft.DropdownOption(key="SUPERVISOR", text="SUPERVISOR"),
                ft.DropdownOption(key="CONSULTA", text="CONSULTA"),
                ft.DropdownOption(key="AUDITOR", text="AUDITOR"),
            ],
        )

        self.txt_password = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            expand=True,
            height=55,
        )

        self.txt_confirmar_password = ft.TextField(
            label="Confirmar contraseña",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            expand=True,
            height=55,
        )

        self.chk_activo = ft.Checkbox(
            label="Usuario activo",
            value=True,
        )

        # ==========================================================
        # BOTONES
        # ==========================================================

        self.btn_guardar = ft.FilledButton(
            "Guardar",
            icon=ft.Icons.SAVE_OUTLINED,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=0),
                bgcolor="#030B16",
            ),
            on_click=lambda e: self.page_ref.run_task(
                self.guardar
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
            "Nuevo Usuario",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="#030B16",
        )

        self.lbl_subtitulo = ft.Text(
            "Ingrese los datos del usuario",
            size=14,
            color="#64748B",
        )

        self.row_password = ft.Row(
                spacing=15,
                controls=[
                    self.txt_password,
                    self.txt_confirmar_password,
                ],
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

                        # ------------------------------------------
                        # HEADER
                        # ------------------------------------------

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

                        # ------------------------------------------
                        # FORMULARIO
                        # ------------------------------------------

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
                                scroll=ft.ScrollMode.AUTO,
                                controls=[

                                    ft.Text(
                                        "Datos del usuario",
                                        size=17,
                                        weight=ft.FontWeight.BOLD,
                                        color="#030B16",
                                    ),

                                    ft.Divider(
                                        height=1,
                                        color="#E2E8F0",
                                    ),

                                    # Usuario / Rol
                                    ft.Row(
                                        spacing=15,
                                        controls=[
                                            self.txt_username,
                                            self.cmb_rol,
                                        ],
                                    ),

                                    # Nombre / Apellido
                                    ft.Row(
                                        spacing=15,
                                        controls=[
                                            self.txt_nombre,
                                            self.txt_apellido,
                                        ],
                                    ),

                                    # Contraseñas
                                    self.row_password,

                                    self.chk_activo,

                                    ft.Divider(
                                        height=1,
                                        color="#E2E8F0",
                                    ),

                                    # Botones
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.END,
                                        spacing=10,
                                        controls=[
                                            self.btn_cancelar,
                                            self.btn_guardar,
                                        ],
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

    def set_mode(self, usuario_id=0):

        self.usuario_id = usuario_id
        self.modo_edicion = usuario_id != 0

        self.limpiar_formulario()

        self.row_password.visible = not self.modo_edicion

        if self.modo_edicion:

            self.lbl_titulo.value = "Editar Usuario"
            self.lbl_subtitulo.value = (
                "Modifique los datos del usuario"
            )

            self.txt_password.label = (
                "Nueva contraseña (opcional)"
            )

            self.txt_confirmar_password.label = (
                "Confirmar nueva contraseña"
            )

            self.page_ref.run_task(
                self.cargar_usuario,
                usuario_id,
            )

        else:

            self.lbl_titulo.value = "Nuevo Usuario"
            self.lbl_subtitulo.value = (
                "Ingrese los datos del nuevo usuario"
            )

            self.txt_password.label = "Contraseña"

            self.txt_confirmar_password.label = (
                "Confirmar contraseña"
            )
        

    # ==============================================================
    # LIMPIAR
    # ==============================================================

    def limpiar_formulario(self):

        self.txt_username.value = ""
        self.txt_nombre.value = ""
        self.txt_apellido.value = ""
        self.cmb_rol.value = ""

        self.txt_password.value = ""
        self.txt_confirmar_password.value = ""

        self.chk_activo.value = True

        self.txt_username.error_text = None
        self.txt_password.error_text = None
        self.txt_confirmar_password.error_text = None

    # ==============================================================
    # CARGAR USUARIO
    # ==============================================================

    async def cargar_usuario(self, usuario_id):

        token = self.page_ref.session.store.get(
            "access_token"
        )

        if not token:
            await self.toast.show(
                           self.page_ref,
                           "Sesión expirada",
                           "error"
                       )
            return

        try:

            headers = {
                "Authorization": f"Bearer {token}"
            }

            url = (
                f"{settings.URL_BACKEND}"
                f"/usuarios/{usuario_id}"
            )

            async with httpx.AsyncClient(
                timeout=10
            ) as client:

                response = await client.get(
                    url,
                    headers=headers,
                )

            if response.status_code == 401:

                await self.toast.show(
                                self.page_ref,
                                "Sesión expirada",
                                "error"
                            )
                return

            if response.status_code != 200:

                await self.toast.show(
                                self.page_ref,
                                "No se pudo cargar el usuario",
                                "error"
                            )
                return

            data = response.json()

            self.txt_username.value = (
                data.get("username") or ""
            )

            self.txt_nombre.value = (
                data.get("nombre") or ""
            )

            self.txt_apellido.value = (
                data.get("apellido") or ""
            )

            self.cmb_rol.value = (
                data.get("rol") or ""
            )

            self.chk_activo.value = bool(
                data.get("activo", True)
            )

            # Por seguridad nunca cargamos una contraseña
            self.txt_password.value = ""
            self.txt_confirmar_password.value = ""

            self.update()

        except httpx.ConnectTimeout:
             await self.toast.show(
                            self.page_ref,
                            "No se pudo conectar con el servidor",
                            "error"
                        )
            

        except Exception as ex:

            print(
                f"Error cargando usuario: {ex}"
            )

            await self.toast.show(
                            self.page_ref,
                              "Error cargando usuario",
                            "error"
                        )

    # ==============================================================
    # VALIDAR
    # ==============================================================

    async def validar(self):

        username = (
            self.txt_username.value or ""
        ).strip()

        password = (
            self.txt_password.value or ""
        )

        confirmar = (
            self.txt_confirmar_password.value or ""
        )

        if not username:

            self.txt_username.error_text = (
                "Ingrese el usuario"
            )

            self.update()
            return False

        # En nuevo usuario la contraseña es obligatoria
        if not self.modo_edicion and not password:

            await  self.toast.show(
                           self.page_ref,
                           "Ingrese contraseña",
                           "alert"
                       )

            self.update()
            return False

        # Si se escribió contraseña, validar confirmación
        if password or confirmar:

            if password != confirmar:

                await self.toast.show(
                    self.page_ref,
                    "las contraseñas no coinciden",
                    "alert"
                 )

                self.update()
                return False

        return True

    # ==============================================================
    # GUARDAR
    # ==============================================================

    async def guardar(self, e=None):

        if not await self.validar():
            return

        token = self.page_ref.session.store.get(
            "access_token"
        )

        if not token:

            await self.toast.show(
                self.page_ref,
                "Sesión expirada",
                "error"
            )
            
            return

        payload = {

            "username": (
                self.txt_username.value or ""
            ).strip(),

            "nombre": (
                self.txt_nombre.value or ""
            ).strip() or None,

            "apellido": (
                self.txt_apellido.value or ""
            ).strip() or None,

            "rol": (
                self.cmb_rol.value or ""
            ).strip() or None,

            "activo": self.chk_activo.value,
        }

        password = (
            self.txt_password.value or ""
        )

        # Solo enviar password si corresponde
        if password:
            payload["password"] = password

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
    
        try:

            async with httpx.AsyncClient(
                timeout=10
            ) as client:

                if self.modo_edicion:

                    url = (
                        f"{settings.URL_BACKEND}"
                        f"/usuarios/{self.usuario_id}"
                    )

                    response = await client.put(
                        url,
                        json=payload,
                        headers=headers,
                    )

                else:

                    url = (
                        f"{settings.URL_BACKEND}"
                        "/usuarios"
                    )
        
                    response = await client.post(
                        url,
                        json=payload,
                        headers=headers,
                    )

            # ------------------------------------------------------
            # RESPUESTAS
            # ------------------------------------------------------

            if response.status_code == 401:

                await self.toast.show(
                    self.page_ref,
                    "Sesión expirada",
                    "error"
                )
                return

            if response.status_code in (200, 201):

             
                await self.toast.show(
                    self.page_ref,
                    "Usuario guardado correctamente"
                    "success"
                )
 
                # Volver al listado
                self.page_ref.run_task(
                    self.volver_despues_de_guardar
                )

                return

            # ------------------------------------------------------
            # ERROR VALIDACIÓN FASTAPI
            # ------------------------------------------------------

            try:

                error_data = response.json()

                print(
                    "ERROR BACKEND:",
                    error_data,
                )

                detail = error_data.get(
                    detail,
                    "Error guardando usuario",
                )

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

                    detail = " | ".join(mensajes)

              
                await self.toast.show(
                    self.page_ref,
                    str(detail),
                    "error"
                )

            except Exception:

                await self.toast.show(
                    self.page_ref,
                    "Error guardando usuario",
                    "error"
                )

        except httpx.ConnectTimeout:
            
            await self.toast.show(
                    self.page_ref,
                    "No se pudo conectar con el servidor",
                    "error"
            )

        except httpx.RequestError as ex:

            print(
                f"Error HTTP: {ex}"
            )

            await self.toast.show(
                            self.page_ref,
                             "Error de conexión con el servidor",
                            "error"
                        )

        except Exception as ex:

            print(
                f"Error guardando usuario: {ex}"
            )
            await self.toast.show(
                            self.page_ref,
                            "Error guardando usuario",
                            "error"
                        )

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

        self.page_ref.layout.change_view(
            "gestionar_usuarios"
        )

        # Recargar listado
        usuarios_view = (
            self.page_ref.layout.views.get(
                "gestionar_usuarios"
            )
        )

        if usuarios_view:

            self.page_ref.run_task(
                usuarios_view.reload_view
            )

    # ==============================================================
    # PEQUEÑA ESPERA PARA MOSTRAR TOAST
    # ==============================================================

    async def _esperar(self):

        import asyncio

        await asyncio.sleep(1)
