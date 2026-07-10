from datetime import datetime

import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings
from views.Gestion_haberes.novedades.modal_novedades_view import ModalNovedad
from utils.formatters import formatear_moneda

class NovedadesView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page

        self.toast = Toast()

        self.modal = ModalNovedad(
            page=self.page_ref,
            on_success=self.cargar_datos
        )

        self.expand = True
        self.bgcolor = "#F1F5F9"
        self.padding = 20

        self.legajo_id = 0

        self.current_page = 1
        self.page_size = 10
        self.total_items = 0

        self.novedades = []

        # ==========================
        # FILTROS
        # ==========================

        self.txt_busqueda = ft.TextField(
            hint_text="Buscar concepto...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=6,
            filled=True,
            bgcolor="white",
            border_color="#CBD5E1",
            expand=True,
            height=36,
            text_size=12,
            content_padding=10,
        )

        # ==========================
        # TABLA
        # ==========================

        self.table = ft.DataTable(

            expand=True,

            column_spacing=15,

            horizontal_margin=10,

            heading_row_height=38,

            data_row_min_height=42,

            data_row_max_height=42,

            heading_row_color="#E2E8F0",

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            vertical_lines=ft.BorderSide(
                1,
                "#E2E8F0"
            ),

            horizontal_lines=ft.BorderSide(
                1,
                "#E2E8F0"
            ),

            heading_text_style=ft.TextStyle(
                size=11,
                weight=ft.FontWeight.BOLD,
                color="#0F172A"
            ),

            columns=[


                ft.DataColumn(ft.Text("Fecha desde", size=11)),
             
                ft.DataColumn(ft.Text("Fecha hasta", size=11)),

                ft.DataColumn(ft.Text("Legajo Nº", size=11)),

                ft.DataColumn(ft.Text("Apellido y nombre", size=11)),


                ft.DataColumn(ft.Text("Código", size=11)),

                ft.DataColumn(ft.Text("Concepto", size=11)),

                ft.DataColumn(ft.Text("Cantidad", size=11)),

                ft.DataColumn(ft.Text("Valor", size=11)),

                ft.DataColumn(ft.Text("Acciones", size=11)),
            ],

            rows=[]
        )

        self.lbl_total = ft.Text(
            "Total: 0",
            size=11,
            color="#64748B"
        )

        self.lbl_page = ft.Text(
            "",
            size=11,
            color="#475569"
        )

        self.content = self.build()

    # =======================================================
    # BUILD
    # =======================================================

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

    # =======================================================
    # HEADER
    # =======================================================

    def header(self):

        return ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            controls=[

                ft.Column(

                    spacing=1,

                    controls=[

                        ft.Text(
                            "Novedades",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Administración de novedades",
                            size=11,
                            color="#64748B"
                        )
                    ]
                ),

                ft.FilledButton(

                    "Nuevo",

                    icon=ft.Icons.ADD,

                    height=36,

                    style=ft.ButtonStyle(

                        bgcolor="#030B16",

                        shape=ft.RoundedRectangleBorder(
                            radius=0
                        )
                    ),

                    on_click=lambda e:
                    self.page_ref.run_task(
                        self.abrir_modal
                    )
                )
            ]
        )

    # =======================================================
    # FILTROS
    # =======================================================

    def filtros(self):

        return ft.Container(

            bgcolor="white",

            padding=10,

            content=ft.Row(

                controls=[

                    self.txt_busqueda,

                    #self.chk_activos,

                    ft.FilledButton(

                        "Buscar",

                        icon=ft.Icons.SEARCH,

                        height=36,

                        style=ft.ButtonStyle(

                            bgcolor="#030B16",

                            shape=ft.RoundedRectangleBorder(
                                radius=0
                            )
                        ),

                       # on_click=self.buscar
                    )
                ]
            )
        )

    # =======================================================
    # TABLA
    # =======================================================

    def grilla(self):

        return ft.Container(

            expand=True,

            bgcolor="white",

            padding=8,

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
                                "Listado de novedades",
                                size=13,
                                weight=ft.FontWeight.BOLD
                            ),

                            self.lbl_total
                        ]
                    ),

                    ft.Divider(),

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
                                icon=ft.Icons.CHEVRON_LEFT,
                                #on_click=self.prev_page
                            ),

                            self.lbl_page,

                            ft.IconButton(
                                icon=ft.Icons.CHEVRON_RIGHT,
                                #on_click=self.next_page
                            )
                        ]
                    )
                ]
            )
        )
    # =======================================================
# CARGA
# =======================================================

    async def load(self) :

        self.legajo_id =0

        self.current_page = 1

        await self.listar()


    async def buscar(self, e):

        self.current_page = 1

        await self.load_data()


    async def listar(self, e=None):
        periodo= '202607'
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

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    f"{settings.URL_BACKEND}/novedades",
                     params={
                        "periodo": periodo
                    },
                    headers=headers
                )

            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API: {response.status_code}",
                    "error"
                )

                return

            self.novedades = response.json()

            self.total_items = len(self.novedades)

            await self.load_data()

        except Exception as ex:

            print(ex)

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )


    async def load_data(self):

        self.table.rows.clear()

        texto = self.txt_busqueda.value.lower().strip()

        #activos = self.chk_activos.value

        datos = self.novedades

        if texto:

            datos = [

                x for x in datos

                if texto in str(
                    x.get(
                        "concepto",
                        ""
                    )
                ).lower()
            ]

        """  if activos:

            datos = [

                x for x in datos

                if x.get(
                    "activo",
                    True
                )
            ]
 """
        self.total_items = len(datos)

        inicio = (self.current_page - 1) * self.page_size

        fin = inicio + self.page_size

        pagina = datos[inicio:fin]

        for item in pagina:
    
            self.table.rows.append(

                ft.DataRow(

                    cells=[

                        ft.DataCell(
                                 ft.Text(
                                        self.formatear_fecha(item.get("fecha_desde")),
                                        size=11,
                                    )
                        ),

                          ft.DataCell(
                                 ft.Text(
                                        self.formatear_fecha(item.get("fecha_hasta")),
                                        size=11,
                                    )
                        ),

                        ft.DataCell(
                            ft.Text(
                                str(
                                    item.get(
                                        "legajo_id",
                                        ""
                                    )
                                ),
                                size=11
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                item.get(
                                    "ayn",
                                    ""
                                ),
                                size=11
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                item.get(
                                    "codigo_concepto",
                                    ""
                                ),
                                size=11
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                item.get(
                                    "concepto",
                                    ""
                                ),
                                size=11
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                str(
                                    item.get(
                                        "cantidad",
                                        ""
                                    )
                                ),
                                size=11
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                f"{formatear_moneda(item.get('valor', 0))}",
                                size=11
                            )
                        ),
                        
                        ft.DataCell(

                            ft.Row(

                                spacing=0,

                                controls=[

                                    ft.IconButton(

                                        icon=ft.Icons.EDIT,

                                        icon_size=18,

                                        tooltip="Editar",

                                        on_click=lambda e,
                                        x=item: self.page_ref.run_task(
                                            self.editar,
                                            x
                                        )
                                    ),

                                    ft.IconButton(

                                        icon=ft.Icons.DELETE,

                                        icon_size=18,

                                        icon_color="red",

                                        tooltip="Eliminar",

                                        on_click=lambda e,
                                        x=item: self.page_ref.run_task(
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

        total_paginas = max(
            1,
            (self.total_items + self.page_size - 1) // self.page_size
        )

        self.lbl_total.value = f"Total: {self.total_items}"

        self.lbl_page.value = f"{self.current_page}/{total_paginas}"

        self.page_ref.update()

    async def cargar_datos(self):
        await self.listar()


    async def abrir_modal(self):

        await self.modal.abrir(
           
        )


    async def editar(self, item):

        await self.modal.abrir(item)


    async def next_page(self, e):

        total_paginas = max(
            1,
            (self.total_items + self.page_size - 1) // self.page_size
        )

        if self.current_page < total_paginas:

            self.current_page += 1

            await self.load_data()


    async def prev_page(self, e):

        if self.current_page > 1:

            self.current_page -= 1

            await self.load_data()
   
    def formatear_fecha(self, fecha):
        if not fecha:
            return ""

        return datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
    
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
            f"{settings.URL_BACKEND}/novedades/{item_id}"
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
                    "Concepto eliminado correctamente",
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
    
