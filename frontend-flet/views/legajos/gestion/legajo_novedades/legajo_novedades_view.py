import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings
from views.legajos.gestion.legajo_novedades.modal_legajo_novedad import  ModalLegajoNovedad
class LegajoNovedadesView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page

        self.toast = Toast()

        self.modal = ModalLegajoNovedad(
            page=self.page_ref,
            on_success=self.cargar_datos
        )
 
        self.legajo_id = 0

        self.expand = True

        self.bgcolor = "#F1F5F9"

        self.padding = 20

        self.current_page = 1

        self.page_size = 10

        self.total_items = 0

        self.novedades = []

        # ==========================
        # FILTROS
        # ==========================

        self.txt_busqueda = ft.TextField(
            hint_text="Buscar novedad",
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
                    ft.Text(
                        "Concepto",
                        size=11
                    )
                ),

                ft.DataColumn(
                    ft.Text(
                        "Cantidad",
                        size=11
                    )
                ),

                ft.DataColumn(
                    ft.Text(
                        "Valor",
                        size=11
                    )
                ),

                ft.DataColumn(
                    ft.Text(
                        "Período",
                        size=11
                    )
                ),

               

                ft.DataColumn(
                    ft.Text(
                        "Acciones",
                        size=11
                    )
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

        """  page.run_task(
            self.listar
        ) """

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
                            "Legajo Novedades",
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

                            bgcolor="#030B16",

                            shape=ft.RoundedRectangleBorder(
                                radius=0
                            )
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
                                ft.Icons.CHEVRON_LEFT
                            ),

                            self.lbl_page,

                            ft.IconButton(
                                ft.Icons.CHEVRON_RIGHT
                            )
                        ]
                    )
                ]
            )
        )
    async def buscar(self, e):

        await self.load_data()

        self.page_ref.update()
    
    async def abrir_modal(self):
        await self.modal.abrir(
            legajo_id=self.legajo_id
        )

    async def cargar_datos(self):
        await self.listar()

    async def next_page(self, e):
        pass

    async def prev_page(self, e):
        pass

    async def listar(self, e=None):

        token = settings.TOKEN

        if not token:

            await self.toast.show(
                self.page_ref,
                "Sesión expirada",
                "error"
            )

            return

        url = (
            f"{settings.URL_BACKEND}"
            f"/legajos/"
            f"{self.legajo_id}"
            f"/novedades"
        )

        headers = {

            "Authorization":
            f"Bearer {token}"
        }

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    headers=headers
                )

            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API: {response.status_code}",
                    "error"
                )

                return

            data = response.json()

            self.novedades = [

                {

                    "id":
                        x.get("id"),

                    "legajo_id":
                        x.get("legajo_id"),

                    "cantidad":
                        x.get("cantidad", 0),

                    "valor":
                        x.get("valor", 0),

                    "periodo":
                        x.get("periodo", ""),

                    "activo":
                        x.get("activo", False),

                    "estado":
                        x.get("activo", ""),

                    "concepto":
                        (
                            x.get("concepto")
                            or {}
                        ).get(
                            "nombre",
                            ""
                        )
                }

                for x in data
            ]

            self.current_page = 1

           # await self.load_data()

            self.page_ref.update()

        except Exception as ex:

            print(ex)

            await self.toast.show(

                self.page_ref,

                str(ex),

                "error"
            )

    async def load(
        self,
        legajo_id
    ):

       self.legajo_id=legajo_id
       await self.listar()

    async def load_data(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{settings.URL_BACKEND}/legajos/{self.legajo_id}/novedades"
            )

        if r.status_code == 200:
            self.table.rows.clear()

            for item in r.json():
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item["tipo"])),
                            ft.DataCell(ft.Text(str(item["fecha_desde"]))),
                            ft.DataCell(ft.Text(str(item["fecha_hasta"] or ""))),
                            ft.DataCell(ft.Text(item["descripcion"] or "")),
                        ]
                    )
                )

            self.page.update()