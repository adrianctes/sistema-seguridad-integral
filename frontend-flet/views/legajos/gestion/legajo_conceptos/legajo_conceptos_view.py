import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings
from utils.permisos import tiene_permiso
from views.legajos.gestion.legajo_conceptos.modal_legajo_concepto import (
    ModalLegajoConcepto
)


class LegajoConceptosView(ft.Container):

    def __init__(self, page):

        super().__init__()

        # =====================================================
        # PAGE
        # =====================================================

        self.page_ref = page

        # =====================================================
        # MODAL
        # =====================================================

        self.modal = ModalLegajoConcepto(
            page=self.page_ref,
            on_success=self.cargar_datos
        )

        # =====================================================
        # TOAST
        # =====================================================

        self.toast = Toast()

        # =====================================================
        # DATOS
        # =====================================================

        self.legajo_id = 0
        self.conceptos = []

        self.expand = True
        self.bgcolor = "#F1F5F9"
        self.padding = 20

        # =====================================================
        # PAGINACIÓN
        # =====================================================

        self.current_page = 1
        self.page_size = 10
        self.total_items = 0

        # =====================================================
        # PERMISOS
        # =====================================================

        self.permiso_crear = False
        self.permiso_editar = False
        self.permiso_eliminar = False

        # =====================================================
        # FILTROS
        # =====================================================

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

        # =====================================================
        # BOTÓN NUEVO
        # =====================================================

        self.boton_nuevo = ft.FilledButton(
            "Nuevo",
            margin=ft.Margin(0, 0, 10, 0),
            icon=ft.Icons.ADD,
            width=110,
            height=36,
            disabled=True,
            on_click=lambda e:
                self.page_ref.run_task(
                    self.abrir_modal
                ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(
                    radius=0
                ),
                bgcolor="#030B16",
                padding=12
            )
        )

        # =====================================================
        # TABLA
        # =====================================================

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

                ft.DataColumn(
                    ft.Text("Cantidad", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Valor", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Activo", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Acciones", size=11)
                ),
            ],

            rows=[]
        )

        # =====================================================
        # PAGINACIÓN
        # =====================================================

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

        # =====================================================
        # CONTENIDO
        # =====================================================

        self.content = self.build()

        # =====================================================
        # CARGA INICIAL
        # =====================================================

        page.run_task(
            self.listar
        )

    # =========================================================
    # BUILD
    # =========================================================

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

    # =========================================================
    # HEADER
    # =========================================================

    def header(self):

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[

                ft.Column(
                    spacing=1,
                    controls=[

                        ft.Text(
                            "Legajo Conceptos",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Administración de conceptos del legajo",
                            size=11,
                            color="#64748B"
                        )
                    ]
                ),

                self.boton_nuevo
            ]
        )

    # =========================================================
    # FILTROS
    # =========================================================

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

    # =========================================================
    # GRILLA
    # =========================================================

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
                                "Listado de conceptos",
                                size=13,
                                weight=ft.FontWeight.BOLD
                            ),

                            self.lbl_total
                        ]
                    ),

                    ft.Divider(
                        height=1
                    ),

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

    # =========================================================
    # LISTAR
    # =========================================================

    async def listar(self, e=None):

        token = self.page_ref.session.store.get(
            "access_token"
        )

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
            f"/legajos/{self.legajo_id}/conceptos"
        )

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

            self.conceptos = [

                {
                    "id": x.get("id"),

                    "legajo_id": x.get(
                        "legajo_id"
                    ),

                    "cantidad": x.get(
                        "cantidad"
                    ),

                    "valor": x.get(
                        "valor",
                        0.0
                    ),

                    "activo": x.get(
                        "activo",
                        False
                    ),

                    "concepto_id": (
                        x.get("concepto") or {}
                    ).get("id"),

                    "codigo": (
                        x.get("concepto") or {}
                    ).get(
                        "codigo",
                        ""
                    ),

                    "nombre": (
                        x.get("concepto") or {}
                    ).get(
                        "nombre",
                        ""
                    )
                }

                for x in data
            ]

            self.current_page = 1

            self.load_data()

            self.page_ref.update()

        except Exception as ex:

            print(ex.args)

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )

    # =========================================================
    # LOAD
    # =========================================================

    async def load(
        self,
        legajo_id
    ):

        # -----------------------------------------------------
        # GUARDAMOS EL LEGAJO
        # -----------------------------------------------------

        self.legajo_id = legajo_id

        # -----------------------------------------------------
        # PERMISO CREAR
        # -----------------------------------------------------

        self.permiso_crear = tiene_permiso(
            self.page_ref,
            "LEGAJOS_CONCEPTOS_APLICADOS_CREAR"
        )

        # -----------------------------------------------------
        # PERMISO EDITAR
        # -----------------------------------------------------

        self.permiso_editar = tiene_permiso(
            self.page_ref,
            "LEGAJOS_CONCEPTOS_APLICADOS_EDITAR"
        )

        # -----------------------------------------------------
        # PERMISO ELIMINAR
        # -----------------------------------------------------

        self.permiso_eliminar = tiene_permiso(
            self.page_ref,
            "LEGAJOS_CONCEPTOS_APLICADOS_ELIMINAR"
        )

        # -----------------------------------------------------
        # DEBUG
        # -----------------------------------------------------

        print(
            "PERMISOS LEGAJO CONCEPTOS:",
            {
                "CREAR": self.permiso_crear,
                "EDITAR": self.permiso_editar,
                "ELIMINAR": self.permiso_eliminar
            }
        )

        # -----------------------------------------------------
        # ACTUALIZAR BOTÓN NUEVO
        # -----------------------------------------------------

        self.actualizar_boton_nuevo()

        # -----------------------------------------------------
        # CARGAR DATOS
        # -----------------------------------------------------

        await self.listar()

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load_data(self):

        self.table.rows.clear()

        activos = self.chk_activos.value

        datos = self.conceptos

        # -----------------------------------------------------
        # FILTRO ACTIVOS
        # -----------------------------------------------------

        if activos is True:

            datos = [
                d
                for d in datos
                if d["activo"]
            ]

        # -----------------------------------------------------
        # FILTRO BUSQUEDA
        # -----------------------------------------------------

        busqueda = (
            self.txt_busqueda.value or ""
        ).strip().lower()

        if busqueda:

            datos = [
                d
                for d in datos
                if busqueda in (
                    d["codigo"] or ""
                ).lower()
                or busqueda in (
                    d["nombre"] or ""
                ).lower()
            ]

        # -----------------------------------------------------
        # PAGINACIÓN
        # -----------------------------------------------------

        self.total_items = len(datos)

        inicio = (
            self.current_page - 1
        ) * self.page_size

        fin = inicio + self.page_size

        datos_pagina = datos[
            inicio:fin
        ]

        # -----------------------------------------------------
        # FILAS
        # -----------------------------------------------------

        for item in datos_pagina:

            self.table.rows.append(

                ft.DataRow(

                    cells=[

                        # -------------------------------------
                        # CÓDIGO
                        # -------------------------------------

                        ft.DataCell(
                            ft.Text(
                                item["codigo"],
                                size=11
                            )
                        ),

                        # -------------------------------------
                        # NOMBRE
                        # -------------------------------------

                        ft.DataCell(
                            ft.Text(
                                item["nombre"],
                                size=11
                            )
                        ),

                        # -------------------------------------
                        # CANTIDAD
                        # -------------------------------------

                        ft.DataCell(
                            ft.Text(
                                str(
                                    item["cantidad"]
                                ),
                                size=11
                            )
                        ),

                        # -------------------------------------
                        # VALOR
                        # -------------------------------------

                        ft.DataCell(

                            ft.Text(

                                f'{float(item["valor"]):,.2f}'
                                .replace(",", "X")
                                .replace(".", ",")
                                .replace("X", "."),

                                size=11
                            )
                        ),

                        # -------------------------------------
                        # ACTIVO
                        # -------------------------------------

                        ft.DataCell(

                            ft.Container(

                                alignment=ft.Alignment.CENTER,

                                content=ft.Icon(

                                    ft.Icons.CHECK
                                    if item["activo"]
                                    else ft.Icons.CLOSE,

                                    size=16
                                )
                            )
                        ),

                        # -------------------------------------
                        # ACCIONES
                        # -------------------------------------

                        self.actualizar_show_menu(
                            item
                        )
                    ]
                )
            )

        # =====================================================
        # TOTALES
        # =====================================================

        self.lbl_total.value = (
            f"Total registros: {self.total_items}"
        )

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
            f"Página {self.current_page} "
            f"de {total_pages}"
        )

    # =========================================================
    # BUSCAR
    # =========================================================

    async def buscar(self, e):

        self.current_page = 1

        self.load_data()

        self.page_ref.update()

    # =========================================================
    # PAGINACIÓN
    # =========================================================

    async def next_page(self, e):

        total_pages = max(
            1,
            (
                self.total_items
                + self.page_size
                - 1
            )
            // self.page_size
        )

        if self.current_page < total_pages:

            self.current_page += 1

            self.load_data()

            self.page_ref.update()

    # =========================================================

    async def prev_page(self, e):

        if self.current_page > 1:

            self.current_page -= 1

            self.load_data()

            self.page_ref.update()

    # =========================================================
    # ABRIR MODAL NUEVO
    # =========================================================

    async def abrir_modal(self):

        if not self.permiso_crear:
            return

        await self.modal.abrir(
            legajo_id=self.legajo_id
        )

    # =========================================================
    # ABRIR MODAL EDITAR
    # =========================================================

    async def abrir_modal_editar(
        self,
        item
    ):

        if not self.permiso_editar:
            return

        await self.modal.abrir(
            legajo_id=self.legajo_id,
            item=item
        )

    # =========================================================
    # CARGAR DATOS DESPUÉS DEL MODAL
    # =========================================================

    async def cargar_datos(self):

        await self.listar()

        self.update()

    # =========================================================
    # CONFIRMAR ELIMINAR
    # =========================================================

    async def confirmar_eliminar(
        self,
        item
    ):

        if not self.permiso_eliminar:
            return

        dialog = ft.AlertDialog(

            modal=True,

            title=ft.Text(
                "Confirmar eliminación"
            ),

            content=ft.Text(
                "¿Realmente desea eliminar "
                "este concepto?"
            ),

            actions_alignment=(
                ft.MainAxisAlignment.END
            ),

            actions=[

                ft.OutlinedButton(
                    "Cancelar",
                    on_click=lambda e:
                        cerrar()
                ),

                ft.FilledButton(
                    "Eliminar",
                    bgcolor="#DC2626",
                    color="white",
                    on_click=lambda e:
                        confirmar()
                )
            ]
        )

        # =====================================================
        # CERRAR
        # =====================================================

        def cerrar():

            dialog.open = False

            self.page_ref.update()

        # =====================================================
        # EJECUTAR
        # =====================================================

        async def ejecutar():

            dialog.open = False

            self.page_ref.update()

            await self.eliminar_item(
                item
            )

        # =====================================================
        # CONFIRMAR
        # =====================================================

        def confirmar():

            self.page_ref.run_task(
                ejecutar
            )

        # =====================================================
        # DIALOG
        # =====================================================

        if dialog not in self.page_ref.overlay:

            self.page_ref.overlay.append(
                dialog
            )

        self.page_ref.dialog = dialog

        dialog.open = True

        self.page_ref.update()

    # =========================================================
    # ELIMINAR ITEM
    # =========================================================

    async def eliminar_item(
        self,
        item
    ):

        if not self.permiso_eliminar:
            return False

        token = self.page_ref.session.store.get(
            "access_token"
        )

        if not token:

            await self.toast.show(
                self.page_ref,
                "Sesión expirada",
                "error"
            )

            return False

        legajo_id = item["legajo_id"]

        item_id = item["id"]

        url = (
            f"{settings.URL_BACKEND}"
            f"/legajos/{legajo_id}"
            f"/conceptos/{item_id}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.delete(
                    url,
                    headers={
                        "Authorization": (
                            f"Bearer {token}"
                        )
                    }
                )

            # -------------------------------------------------
            # ELIMINACIÓN CORRECTA
            # -------------------------------------------------

            if response.status_code in (
                200,
                204
            ):

                await self.toast.show(
                    self.page_ref,
                    "Concepto eliminado correctamente",
                    "success"
                )

                await self.listar()

                self.page_ref.update()

                return True

            # -------------------------------------------------
            # ERROR API
            # -------------------------------------------------

            try:

                data = response.json()

                mensaje = data.get(
                    "detail",
                    "Ocurrió un error"
                )

            except Exception:

                mensaje = (
                    f"Error API "
                    f"({response.status_code})"
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

    # =========================================================
    # ACTUALIZAR BOTÓN NUEVO
    # =========================================================

    def actualizar_boton_nuevo(self):

        self.boton_nuevo.disabled = (
            not self.permiso_crear
        )

        self.boton_nuevo.style = ft.ButtonStyle(

            shape=ft.RoundedRectangleBorder(
                radius=0
            ),

            bgcolor=(
                "#030B16"
                if self.permiso_crear
                else "#9CA3AF"
            )
        )

        self.boton_nuevo.update()

    # =========================================================
    # ACTUALIZAR MENÚ DE ACCIONES
    # =========================================================

    def actualizar_show_menu(
        self,
        item
    ):

        # =====================================================
        # SI NO TIENE NINGUNA ACCIÓN
        # =====================================================

        if (
            not self.permiso_editar
            and not self.permiso_eliminar
        ):

            return ft.DataCell(
                ft.Container(
                    width=40
                )
            )

        # =====================================================
        # ITEMS DEL MENÚ
        # =====================================================

        items = []

        # =====================================================
        # EDITAR
        # =====================================================

        if self.permiso_editar:

            items.append(

                ft.PopupMenuItem(

                    height=30,

                    icon=ft.Icons.EDIT_OUTLINED,

                    content=ft.Text(
                        "Editar",
                        size=11
                    ),

                    on_click=lambda e, i=item:
                        self.page_ref.run_task(
                            self.abrir_modal_editar,
                            i
                        )
                )
            )

        # =====================================================
        # ELIMINAR
        # =====================================================

        if self.permiso_eliminar:

            items.append(

                ft.PopupMenuItem(

                    height=30,

                    icon=ft.Icons.DELETE_OUTLINE,

                    content=ft.Text(
                        "Eliminar",
                        size=11
                    ),

                    on_click=lambda e, i=item:
                        self.page_ref.run_task(
                            self.confirmar_eliminar,
                            i
                        )
                )
            )

        # =====================================================
        # POPUP
        # =====================================================

        return ft.DataCell(

            ft.PopupMenuButton(

                icon=ft.Icons.MORE_VERT,

                items=items
            )
        )