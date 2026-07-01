import asyncio
import flet as ft
import httpx

from core.config import settings
from components.datapicker import DatePickerCustom
from core.constants import TIPO_MOVIMIENTO


class HistoriaLaboralModal(ft.AlertDialog):

    def __init__(self, page, on_success=None):

        super().__init__()

        self.page_ref = page
        self.legajo_id = None
        self.on_success = on_success

        self.modal = True
        self.open = False

        self.bgcolor = "white"

        self.shape = ft.RoundedRectangleBorder(
            radius=0
        )

        self.content_padding = 0

        self.inset_padding = 20

        COMMON_HEIGHT = 55

        # ==========================
        # LOADING
        # ==========================

        self.loading = ft.ProgressRing(
            visible=False
        )

        # ==========================
        # CAMPOS
        # ==========================

        self.ddl_tipo_movimiento = ft.Dropdown(

            label="Tipo Movimiento",

            height=COMMON_HEIGHT,

            options=[
                ft.dropdown.Option(
                    key=str(k),
                    text=v
                )
                for k, v in TIPO_MOVIMIENTO.items()
            ]
        )

        self.fecha = DatePickerCustom(
            page,
            label="Fecha"
        )

        self.txt_observacion = ft.TextField(

            label="Observación",

            multiline=True,

            min_lines=4,

            max_lines=6
        )

        self.lbl_mensaje = ft.Text(

            "",

            visible=False,

            size=13
        )

        # ==========================
        # CONTENIDO
        # ==========================

        self.content = ft.Container(

            width=700,

            padding=20,

            content=ft.Column(

                spacing=15,

                tight=True,

                controls=[

                    ft.Row(

                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Column(

                                spacing=2,

                                controls=[

                                    ft.Text(
                                        "Historia Laboral",
                                        size=18,
                                        weight=ft.FontWeight.BOLD
                                    ),

                                    ft.Text(
                                        "Registrar movimiento laboral",
                                        size=11,
                                        color="#64748B"
                                    ),

                                    self.lbl_mensaje
                                ]
                            ),

                            ft.IconButton(

                                icon=ft.Icons.CLOSE,

                                on_click=self.cerrar
                            )
                        ]
                    ),

                    ft.Divider(),

                    ft.ResponsiveRow(

                        controls=[

                            ft.Container(
                                col={"sm": 12, "md": 6},
                                content=self.ddl_tipo_movimiento
                            ),

                            ft.Container(
                                col={"sm": 12, "md": 6},
                                content=self.fecha
                            ),

                            ft.Container(
                                col=12,
                                content=self.txt_observacion
                            )
                        ]
                    ),

                    ft.Divider(),

                    ft.Row(

                        alignment=ft.MainAxisAlignment.END,

                        controls=[

                            self.loading,

                            ft.OutlinedButton(
                                "Cancelar",
                                on_click=self.cerrar
                            ),

                            ft.FilledButton(
                                "Guardar",
                                on_click=self.guardar
                            )
                        ]
                    )
                ]
            )
        )

        if self not in self.page_ref.overlay:
            self.page_ref.overlay.append(self)

    async def abrir(self, legajo_id):

        self.legajo_id = legajo_id

        self.limpiar()

        self.open = True

        self.page_ref.update()

    async def cerrar(self, e=None):

        self.open = False

        self.page_ref.update()

    def limpiar(self):

        '''self.lbl_mensaje.visible = False
        self.lbl_mensaje.value = ""

        self.ddl_tipo_movimiento.value = None
        self.ddl_tipo_movimiento.error_text = None

        self.txt_observacion.value = ""

        self.fecha.reset()'''
        self.lbl_mensaje.visible = False

        self.lbl_mensaje.value = ""

        self.ddl_tipo_movimiento.value = None

        self.ddl_tipo_movimiento.error_text = None

        self.txt_observacion.value = ""

        self.fecha.reset()

        self.page.update()

    async def validar_formulario(self):

        ok = True

        self.ddl_tipo_movimiento.error_text = None

        if not self.ddl_tipo_movimiento.value:

            self.ddl_tipo_movimiento.error_text = (
                "Seleccione tipo movimiento"
            )

            ok = False

        if not self.fecha.get_value():

            self.fecha.set_error(
                "Seleccione una fecha"
            )

            ok = False

        self.page_ref.update()

        return ok

    async def guardar(self, e):

        if not await self.validar_formulario():
            return

        self.loading.visible = True

        self.page_ref.update()

        try:

            payload = {

                "legajo_id": self.legajo_id,

                "tipo_id": int(
                    self.ddl_tipo_movimiento.value
                ),

                "fecha": self.fecha.get_value(),

                "observacion":
                    self.txt_observacion.value
            }

            ok = await self.api_crear(
                payload
            )

            if ok:

                self.lbl_mensaje.value = (
                    "Guardado correctamente"
                )

                self.lbl_mensaje.color = (
                    "#15803D"
                )

                self.lbl_mensaje.visible = True

                self.page_ref.update()

                await asyncio.sleep(0.8)

                await self.cerrar()

                if self.on_success:

                    await self.on_success()

        finally:

            self.loading.visible = False

            self.page_ref.update()

    async def api_crear(self, payload):

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(

                    f"{settings.URL_BACKEND}/historia-laboral",

                    json=payload,

                    headers={
                        "Authorization":
                        f"Bearer {settings.TOKEN}"
                    }
                )

            if response.status_code in (
                200,
                201
            ):

                return True

            data = response.json()

            self.lbl_mensaje.value = data.get(
                "detail",
                "Error"
            )

        except Exception as ex:

            self.lbl_mensaje.value = str(ex)

        self.lbl_mensaje.color = "#DC2626"

        self.lbl_mensaje.visible = True

        self.page_ref.update()

        return False