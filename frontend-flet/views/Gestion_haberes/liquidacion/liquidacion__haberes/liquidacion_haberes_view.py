from datetime import datetime
from utils.formatters import formatear_fecha
from core.config import settings
from components.alerts import Toast
import httpx
import flet as ft
from .modal_liquidacion_view import LiquidacionDetalleModal


class LiquidacionDeHaberesView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page
        self.toast = Toast()

        self.modal_liquidacion = LiquidacionDetalleModal(
                 self.page_ref
        )

        self.expand = True
        self.bgcolor = "#F1F5F9"
        self.padding = 20

        self.current_page = 1
        self.page_size = 10
        self.total_items = 0

        self.datos = []

        # =====================================
        # FILTROS
        # =====================================

        self.cmb_datos_fijos = ft.Dropdown(
            label="Datos fijos liquidacion",
            expand= True,
            height=36,
            text_size=12,
            options=[]
        )

        self.txt_fecha = ft.TextField(
            label="Fecha",
            value=datetime.now().strftime("%d/%m/%Y"),
            read_only=True,
            width=150,
            height=40,
            filled=True,
            bgcolor="#F8FAFC",
            border_color="#CBD5E1",
            text_size=12,
        )
        self.cmb_legajos = ft.Dropdown(
                label="Legajos",
                width=220,
                value="",
               # on_select=self.cargar_legajo,
                options=[]
            )
        self.chk_estado = ft.Checkbox(
            label="Solo abiertos",
            value=True,
            active_color="#030813"
        )

        # =====================================
        # TABLA
        # =====================================

        self.table = ft.DataTable(

            expand=True,

            heading_row_height=36,

            data_row_min_height=40,
            data_row_max_height=40,

            horizontal_margin=10,
            column_spacing=18,

            border=ft.Border.all(1, "#E2E8F0"),

            vertical_lines=ft.BorderSide(
                1,
                "#E2E8F0"
            ),

            horizontal_lines=ft.BorderSide(
                1,
                "#E2E8F0"
            ),

            heading_row_color="#E2E8F0",

            heading_text_style=ft.TextStyle(
                size=11,
                weight=ft.FontWeight.BOLD,
                color="#0F172A"
            ),

            columns=[

                ft.DataColumn(ft.Text("Fecha", size=11)),
                ft.DataColumn(ft.Text("Período", size=11)),
                #ft.DataColumn(ft.Text("Período", size=11)),
                ft.DataColumn(ft.Text("Modalidad", size=11)),
                ft.DataColumn(ft.Text("Numero", size=11)),
                ft.DataColumn(ft.Text("Leagjo nro", size=11)),
                ft.DataColumn(ft.Text("Apwllido y nombre", size=11)),
                ft.DataColumn(ft.Text("Total haberes", size=11)),
                ft.DataColumn(ft.Text("Total retenciones", size=11)),
                ft.DataColumn(ft.Text("Total neto", size=11)),
                ft.DataColumn(ft.Text("Acciones", size=11)),

            ],

            rows=[]

        )

        self.lbl_total = ft.Text(
            "Total registros: 0",
            size=11,
            color="#64748B"
        )

        self.lbl_page = ft.Text(
            "",
            size=11,
            color="#64748B"
        )

        self.content = self.build()

       # page.run_task(self.listar)

    def build(self):

        return ft.Stack(

            expand=True,

            controls=[

                ft.Column(

                    expand=True,

                    spacing=10,

                    controls=[

                        self.header(),

                        self.filtros(),

                        self.grilla()

                    ]

                ),

                self.toast

            ]

        )
    
    def header(self):

        return ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            controls=[

                ft.Column(

                    spacing=1,

                    controls=[

                        ft.Text(
                            "Liquidaciónes",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),

                       

                    ]

                ),

                ft.FilledButton(

                    "Nuevo",

                    icon=ft.Icons.ADD,

                    width=110,

                    height=36,

                    style=ft.ButtonStyle(
                        bgcolor="#030B16",
                        shape=ft.RoundedRectangleBorder(radius=0)
                    ),

                    on_click=lambda e:
                        self.page_ref.run_task(
                            self.abrir_formulario,
                            None
                        )

                )

            ]

        )     
    
    def filtros(self):

            return ft.Container(

                height=60,

                bgcolor="white",

                padding=10,

                border=ft.Border.all(
                    1,
                    "#E2E8F0"
                ),

                content=ft.Row(

                    spacing=10,

                    controls=[

                        ft.Container(
                            expand=1,
                            content=self.cmb_datos_fijos
                        ),

                        
                        

                        ft.FilledButton(
                           
                            "Buscar",

                            icon=ft.Icons.SEARCH,

                            width=110,

                            height=36,

                            style=ft.ButtonStyle(

                                bgcolor="#030B16",

                                shape=ft.RoundedRectangleBorder(radius=0)

                            ),

                            on_click=self.buscar

                        )

                       
                    ]

                )

            )
    
    def grilla(self):

        return ft.Container(

            expand=True,

            bgcolor="white",

            padding=10,

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            content=ft.Column(

                expand=True,

                spacing=8,

                controls=[

                    ft.Row(

                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Text(

                                "Listado de liquidaciones",

                                size=13,

                                weight=ft.FontWeight.BOLD

                            ),

                            self.lbl_total

                        ]

                    ),

                    ft.Divider(height=1),

                    ft.ListView(

                        expand=True,

                        controls=[

                            self.table

                        ]

                    ),

                    ft.Row(

                        alignment=ft.MainAxisAlignment.END,

                        controls=[

                            ft.IconButton(

                                ft.Icons.CHEVRON_LEFT,

                                on_click=self.prev_page

                            ),

                            self.lbl_page,

                            ft.IconButton(

                                ft.Icons.CHEVRON_RIGHT,

                                on_click=self.next_page

                            )

                        ]

                    )

                ]

            )

        )
    
    async def listar(self, e=None):

        token = settings.TOKEN

        if not token:

            await self.toast.show(
                self.page_ref,
                "Sesión expirada",
                "error"
            )

            return

        headers = {
            "Authorization": f"Bearer {token}"
        }

        url = (
            f"{settings.URL_BACKEND}"
            f"/liquidaciones/datos-fijos/"
            f"{int(self.cmb_datos_fijos.value)}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    headers=headers
                   # follow_redirects=True
                )
   
            if response is None:
                   self.table.rows.clear()
                   return
            if response.status_code == 401:

                self.table.rows.clear()

                await self.toast.show(
                    self.page_ref,
                    "Token inválido",
                    "error"
                )

                return

            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API {response.status_code}",
                    "error"
                )

                return

            self.datos = response.json()

            self.current_page = 1

            self.load_data()

            self.page_ref.update()

        except Exception as ex:

            print(ex)

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )
    
    async def load(self) :

        self.legajo_id =0

        self.current_page = 1

        self.cmb_datos_fijos.options=[]
    
        await self.cargar_datos_fijos_abiertos()
    
        #await self.listar() 

    def load_data(self):

        self.table.rows.clear()

        inicio = (self.current_page - 1) * self.page_size
        fin = inicio + self.page_size

        datos = self.datos[inicio:fin]

        for item in datos:
        
            self.table.rows.append(

                ft.DataRow(

                    cells=[

                        ft.DataCell(
                            ft.Text(formatear_fecha(item["fecha"]), size=11)
                        ),


                        ft.DataCell(
                            ft.Text(item["periodo"], size=11)
                        ),

                        ft.DataCell(
                            ft.Text(item["modalidad"], size=11)
                        ),

                        ft.DataCell(
                            ft.Text(item["numero"], size=11)
                        ),

                        ft.DataCell(
                            ft.Text(item["legajo_id"], size=11)
                        ),

                        ft.DataCell(
                            ft.Text(item["ayn"], size=11)
                        ),

                        ft.DataCell(
                          ft.Text(
                                 f'{float(item["total_haberes"]):,.2f}'
                                 .replace(",", "X")
                                 .replace(".", ",")
                                  .replace("X", "."),
                                 size=11
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                    f'{float(item["total_retenciones"]):,.2f}'
                                    .replace(",", "X")
                                    .replace(".", ",")
                                    .replace("X", "."), size=11)
                        ),

                        ft.DataCell(
                                ft.Text(
                                    f'{float(item["total_neto"]):,.2f}'
                                    .replace(",", "X")
                                    .replace(".", ",")
                                    .replace("X", "."),
                                size=11

                            )

                        ),

                        ft.DataCell(

                            ft.Row(

                                spacing=0,

                                controls=[

                                    ft.IconButton(

                                        icon=ft.Icons.VISIBILITY_OUTLINED,

                                        icon_size=18,

                                        tooltip="Ver",

                                        on_click=lambda e, id=item["id"]:
                                        self.page_ref.run_task(
                                            self.ver_liquidacion,
                                            id
                                        )
                                    ),

                                    ft.IconButton(

                                        icon=ft.Icons.DELETE,

                                        icon_size=18,

                                        icon_color="red",

                                        tooltip="Eliminar",

                                        on_click=lambda e, x=item:
                                            self.page_ref.run_task(
                                                self.confirmar_eliminar,
                                                x
                                            )

                                    )

                                ]

                            )

                        )

                    ]

                )

            )

        self.total_items = len(self.datos)

        self.lbl_total.value = f"Total registros: {self.total_items}"

        total_paginas = max(
            1,
            (self.total_items + self.page_size - 1)
            // self.page_size
        )

        self.lbl_page.value = f"Página {self.current_page} de {total_paginas}"

        self.update()
    
    async def buscar(self, e):

        self.table.rows.clear()
             
        await self.listar()
        
    def limpiar_filtros(self, e):

        # Fecha
        self.chk_estado.value= False

        # Tipo
        self.cmb_tipo.value = None

        # Período
        self.periodo.reset()

        # Refrescar controles
        self.page_ref.update()

        # Opcional: volver a cargar todos los registros
        self.buscar(None)

    async def reload_view(self):

        self.current_page = 1

        self.lbl_total.value = "Total registros: 0"

        self.lbl_page.value = ""

        self.table.rows.clear()

        await self.listar()

        self.update()
    
    async def next_page(self, e):

        total_paginas = max(

            1,

            (len(self.datos) + self.page_size - 1)

            // self.page_size

        )

        if self.current_page < total_paginas:

            self.current_page += 1

            self.load_data()
    
    async def prev_page(self, e):

        if self.current_page > 1:

            self.current_page -= 1

            self.load_data()
    
    async def abrir_formulario(self, item):

        view = self.page_ref.layout.views["crear_editar_liquidacion_haberes"]

        if item is None:

            await view.set_mode(0)

        else:

            await view.set_mode(item["id"])

   

        self.page_ref.layout.change_view(
            "crear_editar_liquidacion_haberes"
        )
    
    async def confirmar_eliminar(self, item):

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                "¿Realmente desea eliminar este registro?"
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[

                ft.OutlinedButton(
                    "Cancelar",
                    on_click=lambda e: cerrar()
                ),

                ft.FilledButton(
                    "Eliminar",
                    bgcolor="#DC2626",
                    color="white",
                    on_click=lambda e: confirmar()
                )
            ]
        )

        def cerrar():

            dialog.open = False

            self.page_ref.update()

        async def ejecutar():

            dialog.open = False

            self.page_ref.update()

            await self.eliminar_item(item)

        def confirmar():

            self.page_ref.run_task(
                ejecutar
            )

        if dialog not in self.page_ref.overlay:
            self.page_ref.overlay.append(dialog)

        self.page_ref.dialog = dialog

        dialog.open = True

        self.page_ref.update()
               
    async def eliminar_item(self, item):

        token = settings.TOKEN
        item_id = item["id"]

        url = (
            f"{settings.URL_BACKEND}/liquidaciones/datos-fijos/{item_id}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.delete(
                    url,
                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )

            # Eliminación correcta
            if response.status_code in (200, 204):

                await self.toast.show(
                    self.page_ref,
                    "Registro eliminado correctamente",
                    "success"
                )

                # recargar listado
                await self.listar()

                self.page_ref.update()

                return True

            # Error API
            try:

                data = response.json()

                mensaje = data.get(
                    "detail",
                    "Ocurrió un error"
                )

            except Exception:

                mensaje = (
                    f"Error API ({response.status_code})"
                )

            await self.toast.show(
                self.page_ref,
                mensaje,
                "error"
            )

            return False

        except Exception as ex:

            print(ex)

            await self.toast.show(
                self.page_ref,
                "Ocurrió un error al intentar eliminar",
                "error"
            )

            return False
    
    async def cargar_datos_fijos_abiertos(self):
        token = settings.TOKEN
    
        if not token:

            await self.toast.show(
                self.page_ref,
                "Sesión expirada",
                "error"
            )

            return
        params = {}   
        params["estado"] = "ABIERTO"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        url = f"{settings.URL_BACKEND}/datos-fijos-liquidacion"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    params=params,
                    headers=headers
                   # follow_redirects=True
                )

            if response is None:
                   self.table.rows.clear()
                   return
            if response.status_code == 401:

                self.table.rows.clear()

                await self.toast.show(
                    self.page_ref,
                    "Token inválido",
                    "error"
                )

                return

            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API {response.status_code}",
                    "error"
                )

                return

            datos = response.json()
            for item in datos:
            
                periodo=  f"{str(item['periodo'])[4:6]}/{str(item['periodo'])[:4]}"
                leyenda = f"{periodo} - {item['modalidad_liquidacion']}/{item['numero']}"
                self.cmb_datos_fijos.options.append(
                    ft.dropdown.Option(
                        key=str(item["id"]),
                        text=leyenda
                    )
                )

            self.page_ref.update()

        except Exception as ex:

            print(ex)

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )

    async def obtener_liquidacion(self, liquidacion_id):

        token = settings.TOKEN

        if not token:

            await self.toast.show(
                self.page_ref,
                "Sesión expirada",
                "error"
            )

            return None

        headers = {
            "Authorization": f"Bearer {token}"
        }

        url = (
            f"{settings.URL_BACKEND}"
            f"/liquidaciones/{liquidacion_id}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    headers=headers
                )

            if response.status_code == 401:

                await self.toast.show(
                    self.page_ref,
                    "Token inválido o expirado",
                    "error"
                )

                return None

            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API: {response.status_code}",
                    "error"
                )

                return None

            return response.json()

        except httpx.RequestError as ex:

            await self.toast.show(
                self.page_ref,
                f"Error de conexión: {ex}",
                "error"
            )

            return None

        except Exception as ex:

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )

            return None

    async def ver_liquidacion(self, liquidacion_id):

        data = await self.obtener_liquidacion(
            liquidacion_id
        )

        if not data:
            return
      
        self.modal_liquidacion.mostrar(
            data
        )