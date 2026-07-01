import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings
import flet as ft

from views.legajos.gestion.legajo_conceptos.modal_legajo_concepto  import  ModalLegajoConcepto


class LegajoConceptosView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page
        self.modal =  ModalLegajoConcepto(page=self.page_ref)
  
        self.toast = Toast()
        self.legajo_id = 0
        self.expand = True
        self.bgcolor = "#F1F5F9"
        self.padding = 20

        self.current_page = 1
        self.page_size = 10
        self.total_items = 0

        self.conceptos = []

        # ==========================
        # FILTROS
        # ==========================
        self.txt_busqueda = ft.TextField(
            hint_text="Buscar concepto",
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

            border=ft.Border.all(1, "#E2E8F0"),
            vertical_lines=ft.BorderSide(1, "#E2E8F0"),
            horizontal_lines=ft.BorderSide(1, "#E2E8F0"),

            heading_text_style=ft.TextStyle(
                size=11,
                weight=ft.FontWeight.BOLD,
                color="#0F172A"
            ),

            columns=[
                        ft.DataColumn(ft.Text("Código", size=11)),
                        ft.DataColumn(ft.Text("Nombre", size=11)),
                        ft.DataColumn(ft.Text("Valor", size=11)),
                        ft.DataColumn(ft.Text("Estado", size=11)),
                        ft.DataColumn(ft.Text("Acciones", size=11)),  # 👈 falta esta
                    ],
            rows=[]
        )

        # ==========================
        # LABELS PAGINACIÓN
        # ==========================
        self.lbl_total = ft.Text("Total: 0", size=11, color="#64748B")

        self.lbl_page = ft.Text("", size=11, color="#475569")

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
                        ft.Text("Legajo Conceptos", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Administración de conceptos del legajo", size=11, color="#64748B"),
                    ]
                ),
                ft.FilledButton(
                                "Nuevo",
                                icon=ft.Icons.ADD,
                                height=36,
                                on_click=lambda e: self.page_ref.run_task(self.abrir_modal),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=0),
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
                            shape=ft.RoundedRectangleBorder(radius=0),
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
            border=ft.Border.all(1, "#E2E8F0"),
            content=ft.Column(
                expand=True,
                spacing=8,
                controls=[

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Listado de conceptos", size=13, weight=ft.FontWeight.BOLD),
                            self.lbl_total
                        ]
                    ),

                    ft.Divider(height=1),

                    ft.ListView(
                        expand=True,
                        controls=[self.table]
                    ),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.IconButton(ft.Icons.CHEVRON_LEFT, on_click=self.prev_page),
                            self.lbl_page,
                            ft.IconButton(ft.Icons.CHEVRON_RIGHT, on_click=self.next_page),
                        ]
                    )
                ]
            )
        )

    # =========================================================
    # API
    # =========================================================
    async def listar(self, e=None):

        token = settings.TOKEN

        if not token:
            await self.toast.show(self.page_ref, "Sesión expirada", "error")
            return

        headers = {"Authorization": f"Bearer {token}"}

        url = f"{settings.URL_BACKEND}/legajos/{self.legajo_id}/conceptos"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)

            if response.status_code != 200:
                await self.toast.show(self.page_ref, f"Error API: {response.status_code}", "error")
                return

            data = response.json()
            self.conceptos = [
                    {
                        "id": x.get("id"),
                        "legajo_id": x.get("legajo_id"),
                        "valor": x.get("valor", 0.0),
                        "activo": x.get("activo", False),

                        "concepto_id": (x.get("concepto") or {}).get("id"),
                        "codigo": (x.get("concepto") or {}).get("codigo", ""),
                        "nombre": (x.get("concepto") or {}).get("nombre", ""),
                    }
                    for x in data
                ]

            self.current_page = 1
            self.load_data()
            self.page_ref.update()

        except Exception as ex:
            print(ex.args)
            await self.toast.show(self.page_ref, str(ex), "error")

    def load_data(self):
    
        self.table.rows.clear()

        datos = self.conceptos
        for item in datos:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item["codigo"], size=11)),
                            ft.DataCell(ft.Text(item["nombre"], size=11)),
                            ft.DataCell(ft.Text(str(item["valor"]), size=11)),

                            ft.DataCell(
                                ft.Icon(
                                    ft.Icons.CHECK if item["activo"] else ft.Icons.CLOSE
                                )
                            ),

                            ft.DataCell(
                                    ft.PopupMenuButton(
                                        icon=ft.Icons.MORE_VERT,
                                        items=[
                                            ft.PopupMenuItem(
                                                content=ft.Text("Editar"),
                                                on_click=lambda e, i=item:
                                                    self.page_ref.run_task(
                                                        self.abrir_modal_editar,
                                                        i
                                                    )
                                            )
                                    ]
                                )
                            )
                        ]
                    )
                )
        self.total_items = len(datos)

        self.lbl_total.value = f"Total registros: {self.total_items}"

        total_pages = max(1, (self.total_items + self.page_size - 1) // self.page_size)

        self.lbl_page.value = f"Página {self.current_page} de {total_pages}"

    async def load(
        self,
        legajo_id
    ):

       self.legajo_id=legajo_id
       await self.listar()
       
    async def buscar(self, e):
        self.load_data()
        self.page_ref.update()

    async def next_page(self, e):
        pass

    async def prev_page(self, e):
        pass

    async def abrir_modal(self):
            await self.modal.abrir(
                legajo_id=self.legajo_id
                
            )

    async def abrir_modal_editar(self, item):
        await self.modal.abrir(
            legajo_id=self.legajo_id,
            item=item
        )

      