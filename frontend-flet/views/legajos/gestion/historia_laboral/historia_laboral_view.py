import flet as ft
import httpx
from core.constants import TIPO_MOVIMIENTO
from views.legajos.gestion.historia_laboral.historia_laboral_modal import HistoriaLaboralModal
from components.alerts import Toast
from core.config import settings
from datetime import datetime


class HistoriaLaboralView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page
        self.modal_historia_laboral = HistoriaLaboralModal(
            page=self.page_ref,
            on_success=self.cargar_historial
)
        self.toast = Toast()
     
        self.expand = True

        self.padding = 20

        self.bgcolor = "#F1F5F9"

        self.legajo_id = None

      

        self.movimientos = []

        # =====================================
        # TABLA
        # =====================================

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
                    ft.Text("Fecha", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Movimiento", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Observación", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Usuario", size=11)
                ),
            ],

            rows=[]
        )

        # =====================================
        # LABELS
        # =====================================

        self.lbl_total = ft.Text(
            "Total: 0",
            size=11,
            color="#64748B"
        )

        # =====================================
        # CONTENIDO
        # =====================================

        contenido = ft.Column(

            expand=True,

            spacing=10,

            controls=[

                # =================================
                # HEADER
                # =================================

                ft.Row(

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                    controls=[

                        ft.Column(

                            spacing=1,

                            controls=[

                                ft.Text(
                                    "Historia Laboral",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color="#0F172A"
                                ),

                                ft.Text(
                                    "Movimientos del empleado",
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
                                    self.modal_historia_laboral.abrir,
                                    self.legajo_id
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
                ),

                # =================================
                # TABLA
                # =================================

                ft.Container(

                    expand=True,

                    bgcolor="white",

                    border_radius=0,

                    border=ft.Border.all(
                        1,
                        "#E2E8F0"
                    ),

                    padding=10,

                    content=ft.Column(

                        expand=True,

                        spacing=8,

                        controls=[

                            ft.Row(

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Listado de Movimientos",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        color="#0F172A"
                                    ),

                                    self.lbl_total
                                ]
                            ),

                            ft.Divider(height=1),

                            ft.Container(

                                expand=True,

                                content=ft.ListView(
                                    expand=True,
                                    controls=[self.table]
                                )
                            ),
                        ]
                    )
                )
            ]
        )

        self.content = ft.Stack(

            expand=True,

            controls=[

                contenido,

                self.toast
            ]
        )

    async def load(self, legajo_id= None, modalidad_pago_id = None ):
  
        if legajo_id:
            self.legajo_id = legajo_id

        self.table.rows.clear()
        self.page.update()

        self.lbl_total.value = "Total: 0"

        self.page_ref.update()

        await self.listar_historial()

    async def listar_historial(self):

        token = settings.TOKEN

        url = (
            f"{settings.URL_BACKEND}"
            f"/legajos/{self.legajo_id}/historia-laboral"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(

                    url,

                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )

            if response.status_code == 401:

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

            self.movimientos = data

            self.load_data()

        except Exception as ex:

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )

    def load_data(self):

        self.table.rows.clear()
        self.page.update()

        self.lbl_total.value = (
            f"Total registros: {len(self.movimientos)}"
        )

        for item in self.movimientos:
            fecha_formateada =  datetime.strptime(
                                     item.get("fecha"),
                                    "%Y-%m-%dT%H:%M:%S"
                                ).strftime("%d/%m/%Y")
            
            self.table.rows.append(

                ft.DataRow(

                    cells=[

                        ft.DataCell(

                            ft.Text(
                                str(
                                    fecha_formateada
                                ),
                                size=11
                            )
                        ),

                        ft.DataCell(

                            ft.Container(

                                content=ft.Text(

                                     TIPO_MOVIMIENTO.get(
                                                item.get("tipo_id"),
                                                "Sin tipo"
                                            ),

                                    color="black",

                                    size=10,

                                    weight=ft.FontWeight.W_500
                                )
                            )
                        ),

                        ft.DataCell(

                            ft.Text(
                                item.get(
                                    "observacion",
                                    ""
                                ),
                                size=11
                            )
                        ),

                        ft.DataCell(

                            ft.Text(
                                item.get(
                                    "usuario",
                                    "-"
                                ),
                                size=11
                            )
                        ),
                    ]
                )
            )

        self.page_ref.update()

    async def cargar_historial(self):

        await self.listar_historial()

        self.page_ref.update()
