import flet as ft
import httpx
from components.alerts import Toast
from core.config import settings

class LoginView:

    def __init__(self, page: ft.Page, on_login, on_change_password):

        self.page = page
        self.on_login = on_login
        self.on_change_password = on_change_password
        self.toast = Toast()

        page.overlay.append(self.toast)

        self.usuario = ""
        
        self.txt_usuario = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            width=360,
            height=50,
            autocorrect=False,
            enable_suggestions=False,
            autofill_hints=[]
        )

        self.txt_password = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            width=360,
            height=50,
            password=True,
            can_reveal_password=True,
            autocorrect=False,
            enable_suggestions=False,
            autofill_hints=[],
                
        )

        self.btn_ingresar = ft.FilledButton(
            "Ingresar",
            width=360,
            height=45,
            on_click=self.login,
        )

    def build(self):
   
        return ft.Container(

            expand=True,

            bgcolor="#F1F5F9",

            alignment=ft.Alignment.CENTER,

            content=ft.Container(

                width=430,
                height=450,

                padding=25,

                border_radius=16,

                bgcolor="white",

                shadow=ft.BoxShadow(
                    blur_radius=20,
                    spread_radius=1,
                ),

                content=ft.Column(

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    spacing=10,

                    controls=[

                        ft.Container(
                            width=55,
                            height=55,
                            border_radius=14,
                            bgcolor="#091224",
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                ft.Icons.SHIELD_OUTLINED,
                                color="white",
                                size=30,
                            ),
                        ),

                        ft.Text(
                            "SAP Seguridad",
                            size=23,
                            weight=ft.FontWeight.BOLD,
                            color="#091224",
                        ),

                        ft.Text(
                            "Iniciar sesión",
                            size=15,
                            color="#64748B",
                        ),

                        ft.Container(
                            height=3
                        ),

                        self.txt_usuario,

                        self.txt_password,

                        self.btn_ingresar,
                    ]
                )
            )
        )

    async def login(self, e):

        usuario = self.txt_usuario.value
        password = self.txt_password.value

        if not usuario or not password:
            await self.toast.show(
                                self.page,
                                "Ingrese usuario y contraseña.",
                                "error"
                            )
            return
       
        self.btn_ingresar.content = ft.ProgressRing(
            width=20,
            height=20,
            stroke_width=2,
        )

        self.page.update()
        try:
            self.btn_ingresar.disabled = True
            resultado = await self.auth(
                    usuario,
                    password
                )

            if not resultado:
                    return

            usuario  =     resultado["usuario"]

            # Guardar token
            token = resultado["access_token"]

            self.page.session.store.set("access_token", token)

            self.page.session.store.set("usuario", usuario)

            # =====================================================
            # VERIFICAR SI DEBE CAMBIAR LA CONTRASEÑA
            # =====================================================

            requiere_cambio_password = resultado.get(
                "requiere_cambio_password",
                False
            )

            if requiere_cambio_password:
                 self.on_change_password()
            else:
                self.on_login()

        finally:
            # Restaurar botón
            self.btn_ingresar.disabled = False
            self.btn_ingresar.content = ft.Text("Ingresar")

            self.page.update()

    async def auth(self, usuario: str, password: str):
        
        url = f"{settings.URL_BACKEND}/auth/login"

        async with httpx.AsyncClient() as client:

            response = await client.post(
               url,
                json={
                    "username": usuario,
                    "password": password
                }
            )


        if response.status_code != 200:
            data = response.json()
           
            await self.toast.show(
                self.page,
                    data.get("detail"),
                    #"Usuario o contraseña incorrectos.",
                    "error"
            )
            return None

        return response.json()

    def limpiar(self):
        self.txt_usuario.value = None
        self.txt_password.value = None

        self.page.update()

        self.txt_usuario.value = ""
        self.txt_password.value = ""

        self.page.update()
    
         