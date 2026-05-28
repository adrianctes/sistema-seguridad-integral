import asyncio

import flet as ft
import httpx

from core.config import settings
from components.datapicker import DatePickerCustom
from core.constants import TIPO_MOVIMIENTO

class HistoriaLaboralModal:

    def __init__(self, page, on_success=None):

        self.page = page

        self.legajo_id = None

        self.on_success = on_success

        # =====================================
        # LOADER
        # =====================================

        self.loading = ft.ProgressRing(
            visible=False
        )

        COMMON_HEIGHT = 55

        # =====================================
        # CAMPOS
        # =====================================
        self.ddl_tipo_movimiento = ft.Dropdown(

                    label="Tipo Movimiento",

                    expand=True,

                    height=COMMON_HEIGHT,

                    options=[

                        ft.dropdown.Option(
                            key=str(key),
                            text=value
                        )

                        for key, value in TIPO_MOVIMIENTO.items()
                    ],
                )
        
        # =====================================
        # FECHA
        # =====================================

        self.fecha = DatePickerCustom(
            self.page,
            label="Fecha"
        )

        # =====================================
        # OBSERVACION
        # =====================================

        self.txt_observacion = ft.TextField(

            label="Observación",

            multiline=True,

            min_lines=4,

            max_lines=6,

            expand=True
        )

        # =====================================
        # MENSAJE
        # =====================================

        self.lbl_mensaje = ft.Text(

            "",

            size=14,

            color=ft.Colors.RED_400,

            visible=False
        )

        # =====================================
        # DIALOG
        # =====================================

        self.dialog = ft.AlertDialog(

            modal=True,

            bgcolor="white",

            shape=ft.RoundedRectangleBorder(
                radius=0
            ),

            content_padding=0,

            inset_padding=20,

            content=ft.Container(

                width=700,

                padding=20,

                content=ft.Column(

                    tight=True,

                    spacing=15,

                    controls=[

                        # =====================================
                        # HEADER
                        # =====================================

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

                        # =====================================
                        # FORM
                        # =====================================

                        ft.ResponsiveRow(

                            controls=[

                                ft.Container(
                                    col={"sm": 12, "md": 6},
                                    content=self.ddl_tipo_movimiento,
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

                        # =====================================
                        # FOOTER
                        # =====================================

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
        )

        self.page.overlay.append(
            self.dialog
        )

    async def abrir(self, legajo_id: int, e=None):
        print(legajo_id)
        self.legajo_id = legajo_id

        self.limpiar()

        self.dialog.open = True

        self.page.update()

    async def cerrar(self, e=None):

        self.dialog.open = False

        self.page.update()

    def limpiar(self):

        self.lbl_mensaje.visible = False

        self.lbl_mensaje.value = ""

        self.ddl_tipo_movimiento.value = None

        self.ddl_tipo_movimiento.error_text = None

        self.txt_observacion.value = ""

        self.fecha.reset()

        self.page.update()

    async def validar_formulario(self):

        valido = True

        self.ddl_tipo_movimiento.error_text = None

        if not self.ddl_tipo_movimiento.value:

            self.ddl_tipo_movimiento.error_text = (
                "Seleccione tipo movimiento"
               
            )

            valido = False

        if not self.fecha.get_value():
            self.fecha.set_error(
                "Seleccione una fecha"
            )

            valido = False

        self.page.update()

        return valido

    async def guardar(self, e):

        if not await self.validar_formulario():
            return

        self.loading.visible = True

        self.page.update()

        try:

            data = {

                "legajo_id": self.legajo_id,

                "tipo_id": int(
                    self.ddl_tipo_movimiento.value
                ),

                "fecha": self.fecha.get_value(),

                "observacion": self.txt_observacion.value
            }

            ok = await self.api_crear(data)

            if ok:

                self.lbl_mensaje.value = (
                    "Movimiento registrado correctamente"
                )

                self.lbl_mensaje.color = "#15803D"

                self.lbl_mensaje.visible = True

                self.page.update()

                await asyncio.sleep(1)

                self.dialog.open = False

                self.page.update()

                if self.on_success:

                    await self.on_success()

        finally:

            self.loading.visible = False

            self.page.update()

    async def api_crear(self, data):

        token = settings.TOKEN

        url = (
            f"{settings.URL_BACKEND}/historia-laboral"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(

                    url,

                    json=data,

                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )

            # =====================================
            # SUCCESS
            # =====================================

            if response.status_code in (200, 201):

                return True

            data = response.json()

            self.lbl_mensaje.value = data.get(
                "detail",
                "Error desconocido"
            )

            self.lbl_mensaje.color = "#DC2626"

            self.lbl_mensaje.visible = True

            self.page.update()

            return False

        except Exception as ex:

            print(ex)

            self.lbl_mensaje.value = str(ex)

            self.lbl_mensaje.color = "#DC2626"

            self.lbl_mensaje.visible = True

            self.page.update()

            return False