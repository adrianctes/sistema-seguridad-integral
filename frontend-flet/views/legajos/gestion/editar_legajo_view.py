from datetime import datetime

import flet as ft
import httpx

from views.legajos.shared import CatalogosService
from core.constants import MODALIDAD_PAGO
from components.alerts import Toast
from core.config import settings


class EditarLegajoView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page

        self.legajo_id = 0

        self.expand = True

        self.bgcolor = "#F1F5F9"

        self.padding = 20
       
        self.selected_item = None
        self.toast = Toast()
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
      
        self.fecha_alta = ft.TextField(
            label="Fecha Ingreso Actual",
            read_only=True
        )
       
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

        self.ddl_modalidad_liquidacion = ft.Dropdown(
            label="Modalidad de liquidacion",
            expand=True,
            height=COMMON_HEIGHT,
            options=[],
        )
        self.ddl_modalidad_pago = ft.Dropdown(
            label="Modalidad de pago",
            expand=True,
            height=COMMON_HEIGHT,
            options=[],
        )
        self.txt_valor_modalidad_pago = ft.TextField(
            label="Valor",
            height=60,
            expand=True,
            value="0.00",
            max_length=10,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.solo_decimal
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
            height=62,
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
            label="Liquida sac",
            value=False
        )

        self.chk_activo = ft.Checkbox(
            label="Activo",
            value=True,
            disabled=True
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
        # =====================================
# CONTENT
# =====================================

        contenido = ft.Column(

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
                                    "Editar",
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

                                    ft.Container(
                                        col={"sm": 12, "md": 6},
                                        content=self.fecha_alta
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
                                        ft.Container(
                                            expand=3,
                                            content=self.ddl_modalidad_liquidacion
                                        ),

                                        ft.Container(
                                            expand=2,
                                            content=self.ddl_modalidad_pago
                                        ),

                                        ft.Container(
                                            expand=1,
                                            content=self.txt_valor_modalidad_pago
                                        )
                                    ]
                                ),


                            ft.Row(
                                spacing=10,
                                controls=[
                                    self.ddl_banco,
                                    self.txt_cbu,
                                ],
                            ),
                            ft.Row(
                            controls=[
                                ft.Container(
                                    expand=2,
                                    content=self.txt_telefono,
                                ),

                                ft.Container(
                                    expand=2,
                                    content=ft.Row(
                                        controls=[

                                            self.chk_sac,
                                            self.chk_activo
                                        ]
                                    )
                                ),
                            ]
                        ),

                            #ft.Row([
                            #    self.chk_sac,
                            #    self.chk_activo
                            #]),

                            ft.Divider(),

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

        # =====================================
        # STACK FINAL
        # =====================================

        self.content = ft.Stack(

            expand=True,

            controls=[

                contenido,

                self.toast
            ]
        )   
    async def load(self, legajo_id: None , modalidad_pago_id = None):
        self.limpiar()
        await CatalogosService.refresh()
        await self.cargar_banco()
        await self.cargar_categoria()
        await self.cargar_modalidad_liquidacion()
        await self.cargar_modalidad_pago()
   
        item =  await self.obtener_legajo_by_id(legajo_id)
    
        self.editar(item)

        #self.update()
    def limpiar(self):

        self.fecha_alta.value= ""
    
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

        self.ddl_modalidad_liquidacion.value = None

        self.ddl_sexo.error_text = None

        self.ddl_categoria.error_text = None

        self.ddl_modalidad_liquidacion.error_text = None

        self.chk_sac.value = False

        self.chk_activo.value = True

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

        if not self.ddl_modalidad_liquidacion.value:
            self.ddl_modalidad.error_text = "Seleccione modalidad"
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
                "modalidad_liquidacion_id": self.ddl_modalidad_liquidacion.value,
                "sac": self.chk_sac.value,
                "activo": self.chk_activo.value,
                "telefono": self.txt_telefono.value,
                "banco_id" : self.ddl_banco.value,
                "cbu": self.txt_cbu.value,
                "modalidad_pago_id": self.ddl_modalidad_pago.value,
                "valor_modalidad_pago": self.txt_valor_modalidad_pago.value
            }

            ok = await self.api_editar(data)

            if ok:
                await self.toast.show(
                    self.page_ref,
                     "Se guardó correctamente",
                    "success"
                )


                self.lbl_mensaje.color = "#15803D"

                self.lbl_mensaje.visible = True

                self.page_ref.update()

                #await asyncio.sleep(1)

               # self.page_ref.layout.change_view(
               #     "legajos"
               # )

        finally:

            self.loading.visible = False

            self.page_ref.update()
   
    async def api_editar(self, data):

        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/legajos/{self.legajo_id}"

        async with httpx.AsyncClient() as client:

            response = await client.put(
                url,
                json=data,
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        return response.status_code in (200, 201)
    
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

    async def cargar_modalidad_liquidacion(self):
        self.ddl_modalidad_liquidacion.options = [

                ft.dropdown.Option(
                    key=str(item["id"]),
                    text=item["nombre"]
                )

                for item in CatalogosService.modalidades_liquidacion
            ]

        self.page_ref.update()

    async def cargar_modalidad_pago(self):
        self.ddl_modalidad_pago.options = [

                ft.dropdown.Option(
                    key=str(item["id"]),
                    text=item["nombre"]
                )

                for item in MODALIDAD_PAGO
            ]

        self.page_ref.update()
   
    def solo_decimal(self, e):
        valor = e.control.value

        permitido = ""

        separador = False

        for c in valor:

            if c.isdigit():
                permitido += c

            elif c in [".", ","] and not separador:
                permitido += "."
                separador = True

        e.control.value = permitido

        e.control.update()

    def solo_numeros(self, e):

        limpio = "".join(
            filter(str.isdigit, e.control.value or "")
        )

        if e.control.value != limpio:

            e.control.value = limpio

            e.control.update()
  
    def force_upper(self, e):

        e.control.value = (
            e.control.value or ""
        ).upper()

        e.control.update()
    
    def editar(self, item):
        self.legajo_id = item["id"]
        self.txt_cuil.value = item["cuil"]
        self.fecha_alta.value = item["fecha_ingreso_actual"]
        self.txt_apellido.value = item["apellido"]
        self.txt_nombre.value = item["nombre"]
        self.ddl_sexo.value = item["sexo"]
        self.ddl_categoria.value = str(item["categoria_id"])
        self.ddl_modalidad_liquidacion.value = str(item["modalidad_liquidacion_id"])
        self.ddl_modalidad_pago.value = str(item["modalidad_pago_id"])
        self.txt_valor_modalidad_pago.value = str(item["valor_modalidad_pago"])
        self.txt_telefono.value = item["telefono"]

        self.chk_sac.value = item["sac"]

        self.chk_activo.value = item["activo"]

        self.page_ref.update()

    async def obtener_legajo_by_id(self,legajo_id:int):
        token = settings.TOKEN
        url = f"{settings.URL_BACKEND}/legajos/{legajo_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
        if response.status_code != 200:
            await self.toast.show(
                    self.page_ref,
                    f"Error API: {response.status_code}",
                    "error"
            )
            return

        data = response.json()
        fecha = data.get("fecha_ingreso_actual")
        fecha_formateada = ""
        if fecha:
            fecha_formateada = datetime.strptime(
                fecha,
                "%Y-%m-%d"
               ).strftime("%d/%m/%Y")

        legajo = {
                    "id" : data.get('id'),
                    "cuil": data.get("cuil", 0),
                    "fecha_ingreso_actual" :  fecha_formateada,
                    "apellido": data.get("apellido", ""),
                    "nombre": data.get("nombre", ""),
                    "sexo": data.get("sexo",""),
                    "categoria_id": data.get("categoria_id"),
                    "modalidad_liquidacion_id":  data.get("modalidad_liquidacion_id"),
                    "telefono": data.get("telefono", ""),
                    "activo": data.get("activo", True),
                    "sac":  data.get("sac", False),
                    "modalidad_pago_id" : data.get("modalidad_pago_id"),
                    "valor_modalidad_pago" : data.get("valor_modalidad_pago")
                }
        
        return legajo
 