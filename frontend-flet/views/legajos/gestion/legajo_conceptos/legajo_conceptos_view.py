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
        self.modal =  ModalLegajoConcepto(page=self.page_ref,
                                          on_success=self.cargar_datos  )
  
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
                        ft.DataColumn(ft.Text("Cantidad", size=11)),
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
                        "cantidad": x.get("cantidad"),
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

    ''' def load_data(self):
    
        self.table.rows.clear()

        activos = self.chk_activos.value

        datos = self.conceptos
        for item in datos:
                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item["codigo"], size=11)),
                            ft.DataCell(ft.Text(item["nombre"], size=11)),
                            ft.DataCell(ft.Text(str(item["cantidad"]), size=11)),
                            ft.DataCell(
                                        ft.Text(
                                            f'{float(item["valor"]):,.2f}'
                                                .replace(",", "X")
                                                .replace(".", ",")
                                                .replace("X", "."),
                                            size=11
                                        )
                                    ),
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
                                                icon=ft.Icons.EDIT_OUTLINED,
                                                content=ft.Text("Editar",
                                                             size=11    ),
                                                on_click=lambda e, i=item:
                                                    self.page_ref.run_task(
                                                        self.abrir_modal_editar,
                                                        i
                                                    )
                                            ),
                                            ft.PopupMenuItem(
                                            height=30,
                                            icon=ft.Icons.DELETE_OUTLINE,
                                            content=ft.Text(
                                                "Eliminar",
                                                size=11
                                            ),
                                            on_click=lambda e, item=item:
                                                self.page_ref.run_task(
                                                    self.confirmar_eliminar,
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

        self.lbl_total.value = f"Total registros: {self.total_items}"

        total_pages = max(1, (self.total_items + self.page_size - 1) // self.page_size)

        self.lbl_page.value = f"Página {self.current_page} de {total_pages}"
        '''
    def load_data(self):

        self.table.rows.clear()

        activos = self.chk_activos.value  # True/False

        datos = self.conceptos

        if activos is True:
            datos = [d for d in datos if d["activo"]]

        for item in datos:
            self.table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["codigo"], size=11)),
                        ft.DataCell(ft.Text(item["nombre"], size=11)),
                        ft.DataCell(ft.Text(str(item["cantidad"]), size=11)),
                        ft.DataCell(
                            ft.Text(
                                f'{float(item["valor"]):,.2f}'
                                    .replace(",", "X")
                                    .replace(".", ",")
                                    .replace("X", "."),
                                size=11
                            )
                        ),
                       ft.DataCell(
                        ft.Container(
                            #width=40,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Icon(
                                ft.Icons.CHECK if item["activo"] else ft.Icons.CLOSE,
                                size=16
                            )
                        )
                    ),
                        ft.DataCell(
                            ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        content=ft.Text("Editar", size=11),
                                        on_click=lambda e, i=item:
                                            self.page_ref.run_task(self.abrir_modal_editar, i)
                                    ),
                                    ft.PopupMenuItem(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        content=ft.Text("Eliminar", size=11),
                                        on_click=lambda e, i=item:
                                            self.page_ref.run_task(self.confirmar_eliminar, i)
                                    ),
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
    
    async def cargar_datos(self):

            await self.listar()

            self.update()
    
    async def confirmar_eliminar(self, item):

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                "¿Realmente desea eliminar este concepto?"
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

        legajo_id = item["legajo_id"]
        item_id = item["id"]

        url = (
            f"{settings.URL_BACKEND}/legajos/{legajo_id}/conceptos/{item_id}"
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
    
