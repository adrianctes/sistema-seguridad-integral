import flet as ft
import httpx

from components.alerts import Toast
from  core.config import settings

class LegajosView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page
      
        self.toast = Toast()

        self.current_page = 1

        self.page_size = 10

        self.total_items = 0


        self.legajos = []

        self.expand = True

        self.bgcolor = "#F1F5F9"

        self.padding = 20


        self.txt_busqueda = ft.TextField(

            hint_text="Buscar por CUIL, apellido o nombre",

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

                ft.DataColumn(ft.Text("Cuil", size=11)),

                ft.DataColumn(ft.Text("Apellido", size=11)),

                ft.DataColumn(ft.Text("Nombre", size=11)),
              
                ft.DataColumn(ft.Text("Telefono", size=11)),

                ft.DataColumn(ft.Text("Estado", size=11)),

                ft.DataColumn(ft.Text("Acciones", size=11))
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
                                    "Legajos",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color="#0F172A"
                                ),

                                ft.Text(
                                    "Administración de personal",
                                    size=11,
                                    color="#64748B"
                                )
                            ]
                        ),

                        ft.FilledButton(

                            "Nuevo",

                            icon=ft.Icons.ADD,

                            height=36,

                            #on_click=self.modal_legajo.abrir_nuevo,
                            on_click=lambda e: self.page_ref.layout.change_view("crear_legajo"),
                           
                          

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
                # FILTROS
                # =================================

                ft.Container(

                    bgcolor="white",

                    border_radius=0,

                    padding=10,

                    border=ft.Border.all(
                        1,
                        "#E2E8F0"
                    ),

                    content=ft.Row(

                        spacing=10,

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
                ),

                # =================================
                # TABLA
                # =================================

                ft.Container(

                    expand=True,

                    bgcolor="white",

                    border_radius=0,

                    border=ft.Border.all(1,"#E2E8F0" ),

                    padding=10,

                    content=ft.Column(

                        expand=True,

                        spacing=8,

                        controls=[

                            ft.Row(

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Listado de Legajos",
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

                            # =================================
                            # PAGINACION
                            # =================================

                            ft.Row(

                                alignment=ft.MainAxisAlignment.END,

                                spacing=2,

                                controls=[

                                    ft.IconButton(
                                        icon=ft.Icons.CHEVRON_LEFT,
                                        icon_size=18,
                                        on_click=self.prev_page
                                    ),

                                    self.lbl_page,

                                    ft.IconButton(
                                        icon=ft.Icons.CHEVRON_RIGHT,
                                        icon_size=18,
                                        on_click=self.next_page
                                    )
                                ]
                            )
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

        page.run_task(self.listar_legajos)

    def load_data(self):

        self.table.rows.clear()

        filtro = (
            self.txt_busqueda.value or ""
        ).lower()

        activos = self.chk_activos.value

        data = [

            x for x in self.legajos

            if (

                filtro in str(x["cuil"]).lower()

                or filtro in x["apellido"].lower()

                or filtro in x["nombre"].lower()

            )

            and (

                x["activo"]
                if activos
                else True
            )
        ]

        self.total_items = len(data)

        self.lbl_total.value = (
            f"Total registros: {self.total_items}"
        )

        start = (
            (self.current_page - 1)
            * self.page_size
        )

        end = start + self.page_size

        paginated = data[start:end]

        for item in paginated:

            activo = item["activo"]

            self.table.rows.append(

                ft.DataRow(

                    cells=[

                        ft.DataCell(
                            ft.Text(
                                str(item["cuil"]),
                                size=11
                            )
                        ),


                        ft.DataCell(
                            ft.Text(
                                item["apellido"],
                                size=11
                            )
                        ),

                        ft.DataCell(
                            ft.Text(
                                item["nombre"],
                                size=11
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(item["telefono"]),
                                size=11
                            )
                        ),
                        ft.DataCell(

                            ft.Container(

                                bgcolor=(
                                    "#DCFCE7"
                                    if activo
                                    else "#FEE2E2"
                                ),

                                border_radius=20,

                                padding=ft.Padding.symmetric(
                                    horizontal=8,
                                    vertical=2
                                ),

                                content=ft.Text(

                                    "Activo"
                                    if activo
                                    else "Inactivo",

                                    color=(
                                        "#166534"
                                        if activo
                                        else "#991B1B"
                                    ),

                                    size=10,

                                    weight=ft.FontWeight.W_500
                                )
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
                                            "Gestionar legajo",
                                            size=11
                                        ),
                                        on_click=lambda e, item=item:
                                            self.page_ref.run_task(
                                                self.abrir_detalle,
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
                                                self.eliminar_legajo,
                                                item
                                            )
                                    ),
                                                                                                   
                                    
                                ]
                            )
                        )
                    ]
                )
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

        self.current_page = 1

        self.load_data()

        self.page_ref.update()

    async def next_page(self, e):

        total_pages = max(
            1,
            (self.total_items + self.page_size - 1)
            // self.page_size
        )

        if self.current_page < total_pages:

            self.current_page += 1

            self.load_data()

            self.page_ref.update()

    async def prev_page(self, e):

        if self.current_page > 1:

            self.current_page -= 1

            self.load_data()

            self.page_ref.update()

    async def listar_legajos(self, e=None):

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

        url = f"{settings.URL_BACKEND}/legajos"

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

            self.legajos = [

                {
                    "id" : x.get('id'),
                    "cuil": x.get("cuil", 0),
                    "apellido": x.get("apellido", ""),
                    "nombre": x.get("nombre", ""),
                    "sexo": x.get("sexo",""),
                    "categoria_id": x.get("categoria_id"),
                    "modalidad_liquidacion_id":  x.get("modalidad_liquidacion_id"),
                    "telefono": x.get("telefono", ""),
                    "activo": x.get("activo", True),
                    "sac":  x.get("sac", False),
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

    async def reload_view(self):

        self.txt_busqueda.value = ""

        self.chk_activos.value = True

        self.current_page = 1

        self.table.rows.clear()

        self.lbl_total.value = "Total: 0"

        self.lbl_page.value = ""

        self.page_ref.update()

        await self.listar_legajos()
    
    '''async def abrir_detalle(self, item):

        gestion = self.page_ref.layout.views[ "gestion_legajo"]
        gestion.legajo_id = item['id']
        await  gestion.load()
    
        self.page_ref.layout.change_view(
            "gestion_legajo"
            )'''
    async def abrir_detalle(self, item):
        #gestion = self.page_ref.layout.views["gestion_legajo"]
        gestion = self.page_ref.layout.views.get('gestion_legajo')
        gestion.set_legajo(item)
        self.page_ref.layout.change_view("gestion_legajo" )

        await gestion.load()
    
    async def eliminar_legajo(self, item):

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

        url = f"{settings.URL_BACKEND}/legajos/{item['id']}"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.delete(
                    url,
                    headers=headers,
                    follow_redirects=True
                )

            # =========================
            # TOKEN INVALIDO
            # =========================

            if response.status_code == 401:

                self.table.rows.clear()

                await self.toast.show(
                    self.page_ref,
                    "Token inválido o expirado",
                    "error"
                )

                return

            # =========================
            # ERROR API
            # =========================

            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API: {response.status_code}",
                    "error"
                )

                return

            # =========================
            # OK
            # =========================

            data = response.json()

            await self.toast.show(
                self.page_ref,
                data.get("message", "Legajo eliminado"),
                "success"
            )

            # refrescar tabla
            await self.listar_legajos()

        except Exception as ex:

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )