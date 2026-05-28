import asyncio
import datetime

import flet as ft
import httpx

from components.datapicker import DatePickerCustom
from core.config import settings
from views.legajos.shared import CatalogosService


class CrearLegajoView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page

        self.legajo_id = 0

        self.expand = True

        self.bgcolor = "#F1F5F9"

        self.padding = 20

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
        self.txt_cuil = ft.TextField(
            label="CUIL",
            expand=True,
            height=70,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=11,
            on_change=self.solo_numeros,
        )

        self.txt_apellido = ft.TextField(
            label="Apellido",
            expand=True,
            height=COMMON_HEIGHT,
            on_change=self.force_upper
        )

        self.txt_nombre = ft.TextField(
            label="Nombre",
            expand=True,
            height=COMMON_HEIGHT,
            on_change=self.force_upper
        )

        self.ddl_sexo = ft.Dropdown(
            label="Sexo",
            expand=True,
            height=COMMON_HEIGHT,
            options=[
                ft.dropdown.Option("M"),
                ft.dropdown.Option("F"),
            ],
        )

        self.ddl_categoria = ft.Dropdown(
            label="Categoría",
            expand=True,
            height=COMMON_HEIGHT,
            options=[],
        )

        self.ddl_modalidad = ft.Dropdown(
            label="Modalidad",
            expand=True,
            height=COMMON_HEIGHT,
            options=[],
        )

        self.txt_telefono = ft.TextField(
            label="Teléfono",
            height=60,
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=15,
            on_change=self.solo_numeros,
        )

        self.txt_cbu = ft.TextField(
            label="CBU",
            height=60,
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=22,
            on_change=self.solo_numeros,
        )

        self.ddl_banco = ft.Dropdown(
            label="Banco",
            expand=True,
            height=COMMON_HEIGHT,
            options=[],
        )


        self.chk_sac = ft.Checkbox(
            label="SAC",
            value=False
        )

        self.lbl_mensaje = ft.Text(
            "",
            size=14,
            color=ft.Colors.RED_400,
            visible=False,
        )

        # =====================================
        # CONTENT
        # =====================================

        self.content = ft.Column(

            expand=True,

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
                                    "Nuevo Legajo",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="#0F172A"
                                ),

                                ft.Text(
                                    "Complete los datos del empleado",
                                    size=11,
                                    color="#64748B",
                                ),
                            ],
                        ),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=lambda e:
                                self.page_ref.layout.change_view(
                                    "legajos"
                                )
                        ),
                    ],
                ),

                # =====================================
                # FORMULARIO
                # =====================================

                ft.Container(

                    bgcolor="white",

                    border=ft.Border.all(
                        1,
                        "#E2E8F0"
                    ),

                    padding=20,

                    content=ft.Column(

                        spacing=15,

                        controls=[

                            self.lbl_mensaje,

                            ft.ResponsiveRow(

                                controls=[

                                    ft.Container(
                                        col={"sm": 12, "md": 6},
                                        content=self.txt_cuil
                                    ),
                                ]
                            ),

                            ft.Row([
                                self.txt_apellido,
                                self.txt_nombre
                            ]),

                            ft.Row([
                                self.ddl_sexo,
                                self.ddl_categoria
                            ]),

                            ft.Row(
                                spacing=10,
                                controls=[
                                    self.ddl_modalidad,
                                    self.txt_telefono,
                                ],
                            ),

                            ft.Row(
                                spacing=10,
                                controls=[
                                    self.ddl_banco,
                                    self.txt_cbu,
                                ],
                            ),

                            ft.Row([
                                self.chk_sac
                            ]),

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

                                        on_click=lambda e:
                                            self.page_ref.layout.change_view(
                                                "legajos"
                                            )
                                    ),

                                    ft.FilledButton(

                                        "Guardar",

                                        on_click=self.guardar,

                                        style=ft.ButtonStyle(
                                            bgcolor="#030B16",
                                            color="white"
                                        )
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        )


    async def load(self):
        self.limpiar()
        await CatalogosService.refresh()
        await self.cargar_banco()
        await self.cargar_categoria()
        await self.cargar_modalidad()


    def limpiar(self):
    
        self.lbl_mensaje.visible = False

        self.lbl_mensaje.value = ""

        self.txt_cuil.value = ""
        
        self.txt_apellido.value = ""

        self.txt_nombre.value = ""

        self.txt_telefono.value = ""

        self.txt_cuil.error_text = None

        self.txt_apellido.error_text = None

        self.txt_nombre.error_text = None

        self.txt_telefono.error_text = None

        self.ddl_sexo.value = None

        self.ddl_categoria.value = None

        self.ddl_modalidad.value = None

        self.ddl_sexo.error_text = None

        self.ddl_categoria.error_text = None

        self.ddl_modalidad.error_text = None

        self.chk_sac.value = False

        self.ddl_banco.value = None

        self.page_ref.update()

    async def validar_formulario(self):

        valido = True

        if not self.txt_cuil.value:
            self.txt_cuil.error = "El CUIL es obligatorio"
            valido = False

        if not self.txt_apellido.value:
            self.txt_apellido.error = "Apellido obligatorio"
            valido = False

        if not self.txt_nombre.value:
            self.txt_nombre.erro = "Nombre obligatorio"
            valido = False

        if not self.ddl_sexo.value:
            self.ddl_sexo.error_text = "Seleccione sexo"
            valido = False

        if not self.ddl_categoria.value:
            self.ddl_categoria.error_text = "Seleccione categoría"
            valido = False

        if not self.ddl_modalidad.value:
            self.ddl_modalidad.error_text = "Seleccione modalidad"
            valido = False
        
        if not self.ddl_banco.value:
            self.ddl_banco.error_text = "Seleccione un banco"
            valido = False

        self.page_ref.update()

        return valido

 
    async def guardar(self, e):

        if not await self.validar_formulario():
            return

        self.loading.visible = True

        self.page_ref.update()

        try:

            data = {
                "cuil": self.txt_cuil.value,
                "apellido": self.txt_apellido.value,
                "nombre": self.txt_nombre.value,
                "sexo": self.ddl_sexo.value,
                "categoria_id": self.ddl_categoria.value,
                "modalidad_liquidacion_id": self.ddl_modalidad.value,
                "sac": self.chk_sac.value,
                "activo": False ,
                "telefono": self.txt_telefono.value,
                "banco_id" : self.ddl_banco.value
            }

            ok = await self.api_crear(data)

            if ok:

                self.lbl_mensaje.value = (
                    "Se guardó correctamente"
                )

                self.lbl_mensaje.color = "#15803D"

                self.lbl_mensaje.visible = True

                self.page_ref.update()

                await asyncio.sleep(1)

                self.page_ref.layout.change_view(
                    "legajos"
                )

        finally:

            self.loading.visible = False

            self.page_ref.update()

    async def api_crear(self, data):

        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/legajos"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(
                    url,
                    json=data,
                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )

            if response.status_code in (200, 201):

                return True

            data = response.json()

            self.lbl_mensaje.value = data.get(
                "detail",
                "Error desconocido"
            )

            self.lbl_mensaje.color = "#DC2626"

            self.lbl_mensaje.visible = True

            self.page_ref.update()

            return False

        except Exception as ex:

            self.lbl_mensaje.value = str(ex)

            self.lbl_mensaje.color = "#DC2626"

            self.lbl_mensaje.visible = True

            self.page_ref.update()

            return False

    async def cargar_banco(self):
        self.ddl_banco.options = [

                ft.dropdown.Option(
                    key=str(item["id"]),
                    text=item["nombre"]
                )

                for item in CatalogosService.bancos
            ]

        self.page_ref.update()
    async def cargar_categoria(self):
        self.ddl_categoria.options = [

                ft.dropdown.Option(
                    key=str(item["id"]),
                    text=item["nombre"]
                )

                for item in  CatalogosService.categorias
            ]

        self.page_ref.update()
    async def cargar_modalidad(self):
        self.ddl_modalidad.options = [

                ft.dropdown.Option(
                    key=str(item["id"]),
                    text=item["nombre"]
                )

                for item in CatalogosService.modalidades
            ]

        self.page_ref.update()
    
    def solo_numeros(self, e):

        limpio = "".join(
            filter(str.isdigit, e.control.value or "")
        )

        if e.control.value != limpio:

            e.control.value = limpio

            e.control.update()

    # =====================================
    # FORCE UPPER
    # =====================================

    def force_upper(self, e):

        e.control.value = (
            e.control.value or ""
        ).upper()

        e.control.update()
    
   