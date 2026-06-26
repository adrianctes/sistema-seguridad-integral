import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings


class ConceptosListView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page

        self.toast = Toast()

        self.expand = True

        self.bgcolor = "#F1F5F9"

        self.padding = 20

        self.current_page = 1

        self.page_size = 10

        self.total_items = 0

        self.conceptos = []

        self.txt_busqueda = ft.TextField(

            hint_text="Buscar nombre",

            prefix_icon=ft.Icons.SEARCH,

            border_radius=6,

            filled=True,

            bgcolor="white",

            border_color="#CBD5E1",

            expand=True,

            height=36,

            text_size=12,

            content_padding=10
        )
        self.chk_activos = ft.Checkbox(
            label="Solo activos",
            value=True,
            active_color="#030813",
            check_color="white",
            scale=0.9
        )

        # ==========================
        # TABLA
        # ==========================

        self.table = ft.DataTable(

                expand=True,

                column_spacing=18,

                horizontal_margin=10,

                heading_row_height=36,

                data_row_min_height=40,

                data_row_max_height=40,

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

                    ft.DataColumn(
                        ft.Text("Código", size=11)
                    ),

                    ft.DataColumn(
                        ft.Text("Nombre", size=11)
                    ),

                    #ft.DataColumn(
                    #    ft.Text("Orden", size=11)
                    #),

                    ft.DataColumn(
                        ft.Text("Tipo", size=11)
                    ),

                    ft.DataColumn(
                        ft.Text("Novedad", size=11)
                    ),

                    ft.DataColumn(
                        ft.Text("Estado", size=11)
                    ),

                    ft.DataColumn(
                        ft.Text("Acciones", size=11)
                    )
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

        page.run_task(self.listar)

    async def init(self):

        await self.listar()

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
                            "Conceptos",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Administración de conceptos",
                            size=11,
                            color="#64748B"
                        )
                    ]
                ),

                ft.FilledButton(

                            "Nuevo",

                            icon=ft.Icons.ADD,

                            height=36,

                             on_click=lambda e:
                                            self.page_ref.run_task(
                                                self.abrir_formulario,
                                                None
                                            ),
                           
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=0
                                ),
                                bgcolor="#030B16",
                                padding=12
                            )
                        )
            ]
        )

    def filtros(self):

        return ft.Container(

            bgcolor="white",

            padding=10,

            content=ft.Row(

                controls=[

                    self.txt_busqueda,

                    self.chk_activos,

                    ft.FilledButton(

                                "Buscar",

                                icon=ft.Icons.SEARCH,

                                height=36,

                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(
                                        radius=0
                                    ),
                                    bgcolor="#030B16",
                                    padding=10
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

            padding=8,

            border=ft.Border.all(1,"#E2E8F0" ),

            content=ft.Column(

                expand=True,

               spacing=8,

                controls=[

                    ft.Row(

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Listado de Conceptos",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        color="#0F172A"
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
                        spacing=2,
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

        url = f"{settings.URL_BACKEND}/conceptos"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    headers=headers,
                    follow_redirects=True
                )

            if response.status_code == 401:
                self.table.rows.clear()
                await self.toast.show(
                    self.page_ref,
                    "Token inválido o expirado",
                    "error"
                )

                return
           
            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API: {response.status_code}",
                    "error"
                )

                return

            data = response.json()
           
            self.conceptos = [

                {
                    "id" : x.get('id'),
                    "codigo": x.get("codigo", ""),
                    "nombre": x.get("nombre", ""),
                    "califiacacion_concepto_id": x.get("califiacacion_concepto_id", ""),
                    "tipo_calculo": x.get("tipo_calculo",""),
                    "formula": x.get("formula"),
                    "es_novedad": x.get("es_novedad",False),
                    "activo": x.get("activo", False)
                }

                for x in data
            ]

            self.current_page = 1

            self.load_data()

            self.page_ref.update()

        except Exception as ex:

            print("ERROR:", ex)

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )

    def load_data(self):

        self.table.rows.clear()

        datos = self.conceptos

        for item in datos:

            self.table.rows.append(

                ft.DataRow(

                    cells=[

                        ft.DataCell(
                            ft.Text(
                                item["codigo"],
                                 size=11
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                item["nombre"],
                                size=11
                            )
                        ),

                       # ft.DataCell(
                        #    ft.Text(
                        #        str(
                        #            item["orden"]
                        #        )
                        #    )
                        #),

                        ft.DataCell(
                            ft.Text(
                                item["tipo_calculo"],
                                size=11
                            )
                        ),

                        ft.DataCell(

                            ft.Icon(

                                ft.Icons.CHECK if bool(item["es_novedad"]) 
                                               else ft.Icons.CLOSE
                            )
                        ),

                        ft.DataCell(

                            ft.Text(

                                "Activo"

                                if item[
                                    "activo"
                                ]

                                else
                                "Inactivo", 
                                size=11
                            )
                             
                        ),
                         ft.DataCell(

                            ft.PopupMenuButton(

                                icon=ft.Icons.MORE_VERT,

                                icon_size=18,

                                items=[

                                    ft.PopupMenuItem(
                                        height=30,
                                        icon=ft.Icons.VISIBILITY_OUTLINED,
                                        content=ft.Text(
                                            "Gestionar concepto",
                                            size=11
                                        ),
                                        on_click=lambda e, item=item:
                                            self.page_ref.run_task(
                                                self.abrir_formulario,
                                                item
                                            )
                                    ),
                                    ft.PopupMenuItem(),  # divisor
                                    ft.PopupMenuItem(
                                        height=30,
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        content=ft.Text(
                                            "Eliminar",
                                            size=11
                                        ),
                                        on_click=lambda e, item=item:
                                            self.page_ref.run_task(
                                                self.eliminar_concepto,
                                                item
                                            )
                                    ),
                                                                                                   
                                    
                                ]
                            )
                        )
                    
                      ]
                )
            )

        self.total_items = len(datos)

        self.lbl_total.value = (
            f"Total registros: {self.total_items}"
        )
        total_pages = max(
            1,
            (self.total_items + self.page_size - 1)
            // self.page_size
        )

        self.lbl_page.value = (
            f"Página {self.current_page} de {total_pages}"
        )
  
    async def buscar(self, e):

        self.load_data()

        self.page_ref.update()

    async def next_page(self, e):
        pass

    async def prev_page(self, e):
        pass
    async def reload_view(self):

        self.txt_busqueda.value = ""

        self.chk_activos.value = True

        self.current_page = 1

        self.table.rows.clear()

        self.lbl_total.value = "Total: 0"

        self.lbl_page.value = ""

        await self.listar()

        self.update()
    
    async def abrir_formulario(self, item):
        view = self.page_ref.layout.views.get('crear_concepto')
        if not item is None:
            await view.set_mode(item["id"])
        else:
            await view.set_mode(0)
        self.page_ref.layout.change_view("crear_concepto")
       


        