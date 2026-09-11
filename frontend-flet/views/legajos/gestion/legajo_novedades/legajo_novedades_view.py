""" import flet as ft
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

         page.run_task(
            self.listar
        ) 
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

    def cargar_grilla(self, datos):

            self.table.rows.clear()

            for item in datos:

                self.table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(item["concepto"])
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item["cantidad"])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item["valor"])
                                )
                            ),

                            ft.DataCell(
                                ft.Text(
                                    str(item["periodo"])
                                )
                            ),

                            ft.DataCell(
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_size=18,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_size=18,
                                            icon_color="red",
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                )

            self.lbl_total.value = (
                f"Total: {len(datos)}"
            )

            self.page_ref.update()

    def aplicar_filtros(self):

            texto = (
                self.txt_busqueda.value or ""
            ).strip().lower()

            solo_activos = self.chk_activos.value

            datos = self.novedades

            if texto:
                datos = [
                    item
                    for item in datos
                    if texto in item["concepto"].lower()
                ]

            if solo_activos:
                datos = [
                    item
                    for item in datos
                    if item["activo"]
                ]

            self.cargar_grilla(datos)

    async def buscar(self, e):

        self.aplicar_filtros()

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

        token = self.page.session.store.get("access_token")

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


            self.page_ref.update()

        except Exception as ex:

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

            self.page.update() """
import flet as ft
import httpx

from core.config import settings
from shared.toast import Toast
from views.modals.modal_legajo_novedad import ModalLegajoNovedad


class LegajoNovedadesView(ft.Container):

    def __init__(self, page: ft.Page):

        super().__init__(
            expand=True,
            padding=20,
        )

        self.page_ref = page

        # ==========================================================
        # ESTADO
        # ==========================================================

        self.legajo_id = 0

        self.current_page = 1
        self.page_size = 10
        self.total_items = 0

        self.novedades = []
        self.novedades_filtradas = []

        # ==========================================================
        # TOAST
        # ==========================================================

        self.toast = Toast()

        # ==========================================================
        # MODAL
        # ==========================================================

        self.modal = ModalLegajoNovedad(
            page=self.page_ref,
            on_success=self.cargar_datos
        )

        # ==========================================================
        # BUSQUEDA
        # ==========================================================

        self.txt_busqueda = ft.TextField(
            label="Buscar",
            hint_text="Buscar por concepto...",
            prefix_icon=ft.Icons.SEARCH,
            width=300,
            height=50,
            on_submit=self.buscar,
        )

        # ==========================================================
        # SOLO ACTIVOS
        # ==========================================================

        self.chk_activos = ft.Checkbox(
            label="Solo activos",
            value=True,
            on_change=self.buscar,
        )

        # ==========================================================
        # TABLA
        # ==========================================================

        self.table = ft.DataTable(
            expand=True,
            column_spacing=25,
            columns=[
                ft.DataColumn(
                    ft.Text(
                        "Concepto",
                        weight=ft.FontWeight.BOLD
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Cantidad",
                        weight=ft.FontWeight.BOLD
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Valor",
                        weight=ft.FontWeight.BOLD
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Período",
                        weight=ft.FontWeight.BOLD
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Acciones",
                        weight=ft.FontWeight.BOLD
                    )
                ),
            ],
            rows=[],
        )

        # ==========================================================
        # PAGINACION
        # ==========================================================

        self.lbl_total = ft.Text(
            "Total: 0",
            size=13,
            color=ft.Colors.GREY_700,
        )

        self.lbl_page = ft.Text(
            "",
            size=13,
            color=ft.Colors.GREY_700,
        )

        self.btn_anterior = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT,
            tooltip="Página anterior",
            on_click=self.prev_page,
            disabled=True,
        )

        self.btn_siguiente = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT,
            tooltip="Página siguiente",
            on_click=self.next_page,
            disabled=True,
        )

        # ==========================================================
        # LOADING
        # ==========================================================

        self.loading = ft.ProgressRing(
            width=45,
            height=45,
        )

        self.loading_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.loading,
                    ft.Text(
                        "Cargando novedades...",
                        size=14,
                        color=ft.Colors.WHITE,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            ),
            bgcolor="#80000000",
            expand=True,
            visible=False,
        )

        # ==========================================================
        # CONTENIDO
        # ==========================================================

        contenido = ft.Column(
            controls=[
                self.header(),
                self.filtros(),
                self.grilla(),
                self.paginacion(),
            ],
            expand=True,
            spacing=15,
        )

        # ==========================================================
        # STACK
        # ==========================================================

        self.content = ft.Stack(
            expand=True,
            controls=[
                contenido,
                self.loading_container,
                self.toast,
            ],
        )

    # ==============================================================
    # HEADER
    # ==============================================================

    def header(self):

        return ft.Row(
            controls=[
                ft.Text(
                    "Novedades del Legajo",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(expand=True),

                ft.ElevatedButton(
                    "Nueva novedad",
                    icon=ft.Icons.ADD,
                    on_click=lambda e: self.page_ref.run_task(
                        self.abrir_modal
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    # ==============================================================
    # FILTROS
    # ==============================================================

    def filtros(self):

        return ft.Container(
            padding=10,
            bgcolor="#F1F5F9",
            border_radius=8,
            content=ft.Row(
                controls=[
                    self.txt_busqueda,

                    self.chk_activos,

                    ft.ElevatedButton(
                        "Buscar",
                        icon=ft.Icons.SEARCH,
                        on_click=self.buscar,
                    ),

                    ft.ElevatedButton(
                        "Limpiar",
                        icon=ft.Icons.CLEAR,
                        on_click=self.limpiar_filtros,
                    ),
                ],
                spacing=10,
            ),
        )

    # ==============================================================
    # GRILLA
    # ==============================================================

    def grilla(self):

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            padding=10,
            content=ft.ListView(
                expand=True,
                controls=[
                    self.table,
                ],
            ),
        )

    # ==============================================================
    # PAGINACION
    # ==============================================================

    def paginacion(self):

        return ft.Row(
            controls=[
                self.lbl_total,

                ft.Container(expand=True),

                self.btn_anterior,

                self.lbl_page,

                self.btn_siguiente,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    # ==============================================================
    # LOAD
    # ==============================================================

    async def load(self, legajo_id):

        self.legajo_id = legajo_id

        self.loading_container.visible = True

        self.page_ref.update()

        try:

            await self.listar()

        except Exception as ex:

            print(
                f"Error cargando novedades del legajo "
                f"{legajo_id}: {ex}"
            )

            await self.toast.show(
                self.page_ref,
                f"Error cargando novedades: {ex}",
                "error",
            )

        finally:

            self.loading_container.visible = False

            self.page_ref.update()

    # ==============================================================
    # LISTAR
    # ==============================================================

    async def listar(self):

        token = self.page_ref.session.store.get(
            "access_token"
        )

        if not token:

            await self.toast.show(
                self.page_ref,
                "Sesión expirada.",
                "error",
            )

            return

        if not self.legajo_id:

            await self.toast.show(
                self.page_ref,
                "No se indicó el legajo.",
                "error",
            )

            return

        url = (
            f"{settings.URL_BACKEND}"
            f"/legajos/{self.legajo_id}/novedades"
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    headers=headers,
                    timeout=30,
                )

            print(
                f"GET {url} -> "
                f"{response.status_code}"
            )

            if response.status_code == 401:

                await self.toast.show(
                    self.page_ref,
                    "Sesión expirada.",
                    "error",
                )

                return

            if response.status_code != 200:

                try:
                    detalle = response.json().get(
                        "detail",
                        response.text
                    )
                except Exception:
                    detalle = response.text

                await self.toast.show(
                    self.page_ref,
                    f"Error: {detalle}",
                    "error",
                )

                return

            data = response.json()

            if not data:
                data = []

            # ======================================================
            # NORMALIZAR DATOS
            # ======================================================

            self.novedades = [
                {
                    "id": x.get("id"),

                    "legajo_id": x.get(
                        "legajo_id",
                        self.legajo_id
                    ),

                    "cantidad": x.get(
                        "cantidad",
                        0
                    ),

                    "valor": x.get(
                        "valor",
                        0
                    ),

                    "periodo": x.get(
                        "periodo",
                        ""
                    ),

                    "activo": x.get(
                        "activo",
                        False
                    ),

                    "estado": (
                        "Activo"
                        if x.get("activo", False)
                        else "Inactivo"
                    ),

                    "concepto": (
                        x.get("concepto") or {}
                    ).get(
                        "nombre",
                        ""
                    ),

                    "codigo_concepto": (
                        x.get("concepto") or {}
                    ).get(
                        "codigo",
                        x.get(
                            "codigo_concepto",
                            ""
                        )
                    ),

                    "fecha_desde": x.get(
                        "fecha_desde"
                    ),

                    "fecha_hasta": x.get(
                        "fecha_hasta"
                    ),

                    "liquidacion_detalle_id": x.get(
                        "liquidacion_detalle_id"
                    ),
                }
                for x in data
            ]

            # ======================================================
            # INICIALIZAR FILTRO
            # ======================================================

            self.current_page = 1

            self.aplicar_filtros()

        except httpx.RequestError as ex:

            print(
                f"Error de conexión: {ex}"
            )

            await self.toast.show(
                self.page_ref,
                "No se pudo conectar con el servidor.",
                "error",
            )

        except Exception as ex:

            print(
                f"Error inesperado: {ex}"
            )

            await self.toast.show(
                self.page_ref,
                f"Error: {ex}",
                "error",
            )

    # ==============================================================
    # BUSCAR
    # ==============================================================

    async def buscar(self, e=None):

        self.current_page = 1

        self.aplicar_filtros()

        self.page_ref.update()

    # ==============================================================
    # APLICAR FILTROS
    # ==============================================================

    def aplicar_filtros(self):

        texto = (
            self.txt_busqueda.value or ""
        ).strip().lower()

        solo_activos = (
            self.chk_activos.value
        )

        datos = list(
            self.novedades
        )

        # ----------------------------------------------------------
        # FILTRO POR TEXTO
        # ----------------------------------------------------------

        if texto:

            datos = [
                item
                for item in datos
                if texto in (
                    item.get(
                        "concepto",
                        ""
                    ) or ""
                ).lower()
                or texto in (
                    item.get(
                        "codigo_concepto",
                        ""
                    ) or ""
                ).lower()
            ]

        # ----------------------------------------------------------
        # SOLO ACTIVOS
        # ----------------------------------------------------------

        if solo_activos:

            datos = [
                item
                for item in datos
                if item.get(
                    "activo",
                    False
                )
            ]

        self.novedades_filtradas = datos

        self.total_items = len(
            datos
        )

        self.cargar_grilla()

    # ==============================================================
    # CARGAR GRILLA
    # ==============================================================

    def cargar_grilla(self):

        self.table.rows.clear()

        inicio = (
            self.current_page - 1
        ) * self.page_size

        fin = (
            inicio + self.page_size
        )

        datos = (
            self.novedades_filtradas[
                inicio:fin
            ]
        )

        for item in datos:

            # ------------------------------------------------------
            # DETERMINAR SI ESTÁ LIQUIDADA
            # ------------------------------------------------------

            liquidada = (
                item.get(
                    "liquidacion_detalle_id"
                ) is not None
            )

            # ------------------------------------------------------
            # BOTÓN EDITAR
            # ------------------------------------------------------

            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_size=18,
                tooltip=(
                    "Novedad liquidada"
                    if liquidada
                    else "Editar"
                ),
                disabled=liquidada,
                on_click=(
                    None
                    if liquidada
                    else lambda e,
                    item=item:
                    self.editar_novedad(item)
                ),
            )

            # ------------------------------------------------------
            # BOTÓN ELIMINAR
            # ------------------------------------------------------

            btn_eliminar = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_size=18,
                icon_color=ft.Colors.RED,
                tooltip=(
                    "Novedad liquidada"
                    if liquidada
                    else "Eliminar"
                ),
                disabled=liquidada,
                on_click=(
                    None
                    if liquidada
                    else lambda e,
                    item=item:
                    self.eliminar_novedad(item)
                ),
            )

            # ------------------------------------------------------
            # FILA
            # ------------------------------------------------------

            row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(
                            item.get(
                                "concepto",
                                ""
                            )
                        )
                    ),

                    ft.DataCell(
                        ft.Text(
                            str(
                                item.get(
                                    "cantidad",
                                    0
                                )
                            )
                        )
                    ),

                    ft.DataCell(
                        ft.Text(
                            str(
                                item.get(
                                    "valor",
                                    0
                                )
                            )
                        )
                    ),

                    ft.DataCell(
                        ft.Text(
                            str(
                                item.get(
                                    "periodo",
                                    ""
                                )
                            )
                        )
                    ),

                    ft.DataCell(
                        ft.Row(
                            controls=[
                                btn_editar,
                                btn_eliminar,
                            ],
                            spacing=0,
                        )
                    ),
                ]
            )

            self.table.rows.append(
                row
            )

        # ==========================================================
        # TOTAL
        # ==========================================================

        self.lbl_total.value = (
            f"Total: {self.total_items}"
        )

        # ==========================================================
        # PAGINACION
        # ==========================================================

        total_pages = max(
            1,
            (
                self.total_items
                + self.page_size
                - 1
            )
            // self.page_size
        )

        self.lbl_page.value = (
            f"Página "
            f"{self.current_page} "
            f"de "
            f"{total_pages}"
        )

        self.btn_anterior.disabled = (
            self.current_page <= 1
        )

        self.btn_siguiente.disabled = (
            self.current_page >= total_pages
        )

        self.page_ref.update()

    # ==============================================================
    # LIMPIAR FILTROS
    # ==============================================================

    async def limpiar_filtros(self, e=None):

        self.txt_busqueda.value = ""

        self.chk_activos.value = True

        self.current_page = 1

        self.aplicar_filtros()

        self.page_ref.update()

    # ==============================================================
    # SIGUIENTE PAGINA
    # ==============================================================

    async def next_page(self, e=None):

        total_pages = max(
            1,
            (
                self.total_items
                + self.page_size
                - 1
            )
            // self.page_size
        )

        if self.current_page >= total_pages:
            return

        self.current_page += 1

        self.cargar_grilla()

    # ==============================================================
    # PAGINA ANTERIOR
    # ==============================================================

    async def prev_page(self, e=None):

        if self.current_page <= 1:
            return

        self.current_page -= 1

        self.cargar_grilla()

    # ==============================================================
    # ABRIR MODAL
    # ==============================================================

    async def abrir_modal(self):

        if not self.legajo_id:

            await self.toast.show(
                self.page_ref,
                "No se indicó el legajo.",
                "error",
            )

            return

        await self.modal.abrir(
            legajo_id=self.legajo_id
        )

    # ==============================================================
    # DESPUES DE GUARDAR EN EL MODAL
    # ==============================================================

    async def cargar_datos(self):

        await self.listar()

    # ==============================================================
    # EDITAR NOVEDAD
    # ==============================================================

    async def editar_novedad(self, item):


        if item.get(
            "liquidacion_detalle_id"
        ) is not None:

            await self.toast.show(
                self.page_ref,
                "La novedad ya fue liquidada y no puede modificarse.",
                "warning",
            )

            return

        print(
            "Editar novedad:",
            item
        )

        # ==========================================================
        # ACÁ PODÉS ABRIR EL MODAL EN MODO EDICIÓN
        #
        # Ejemplo:
        #
        await self.modal.abrir(
             legajo_id=self.legajo_id,
             novedad_id=item["id"]
         )
        # ==========================================================

    # ==============================================================
    # ELIMINAR NOVEDAD
    # ==============================================================

    async def eliminar_novedad(self, item):

        if item.get(
            "liquidacion_detalle_id"
        ) is not None:

            await self.toast.show(
                self.page_ref,
                "La novedad ya fue liquidada y no puede eliminarse.",
                "warning",
            )

            return

        print(
            "Eliminar novedad:",
            item
        )
