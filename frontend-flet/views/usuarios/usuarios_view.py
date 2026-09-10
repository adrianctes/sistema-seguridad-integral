
import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings


class UsuariosView(ft.Container):

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

        self.usuarios = []

        # ==========================
        # FILTROS
        # ==========================

        self.txt_busqueda = ft.TextField(
            hint_text="Buscar usuario",
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
                    ft.Text("Usuario", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Nombre", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Apellido", size=11)
                ),

                ft.DataColumn(
                    ft.Text("Rol", size=11)
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

        # ==========================
        # TOTALES / PAGINACION
        # ==========================

        self.lbl_total = ft.Text(
            "Total registros: 0",
            size=11,
            color="#64748B"
        )

        self.lbl_page = ft.Text(
            "",
            size=11,
            color="#475569"
        )

        # ==========================
        # CONSTRUIR
        # ==========================

        self.content = self.build()

        # ==========================
        # CARGAR
        # ==========================

        page.run_task(self.listar)

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
                            "Usuarios",
                            size=18,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Administración de usuarios",
                            size=11,
                            color="#64748B"
                        )
                    ]
                ),

                ft.FilledButton(

                    "Nuevo",

                    margin=ft.Margin(
                        0,
                        0,
                        10,
                        0
                    ),

                    icon=ft.Icons.ADD,

                    width=110,

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

                        bgcolor="#030B16"
                    )
                )
            ]
        )

    # =========================================================
    # FILTROS
    # =========================================================

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

                controls=[

                    self.txt_busqueda,

                    self.chk_activos,

                    ft.FilledButton(

                        "Buscar",

                        icon=ft.Icons.SEARCH,

                        width=110,

                        height=36,

                        style=ft.ButtonStyle(

                            shape=ft.RoundedRectangleBorder(
                                radius=0
                            ),

                            bgcolor="#030B16"
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
                                "Listado de Usuarios",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color="#0F172A"
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

                                tooltip="Página anterior",

                                on_click=self.prev_page
                            ),

                            self.lbl_page,

                            ft.IconButton(

                                ft.Icons.CHEVRON_RIGHT,

                                tooltip="Página siguiente",

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

    async def listar(self,filtro=None, e=None):

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

        url = f"{settings.URL_BACKEND}/usuarios"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    headers=headers,
                    params=filtro,
                    follow_redirects=True
                )
          
            # ==========================
            # NO AUTORIZADO
            # ==========================

            if response.status_code == 401:

                self.table.rows.clear()

                await self.toast.show(
                    self.page_ref,
                    "Token inválido o expirado",
                    "error"
                )

                return

            # ==========================
            # ERROR API
            # ==========================

            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API: {response.status_code}",
                    "error"
                )

                return

            # ==========================
            # RESPUESTA
            # ==========================

            data = response.json()
    
            self.usuarios = [

                {
                    "id": x.get("id"),

                    "usuario": x.get(
                        "username",
                        ""
                    ),

                    "nombre": x.get(
                        "nombre",
                        ""
                    ),

                    "apellido": x.get(
                        "apellido",
                        ""
                    ),

                    "rol": x.get(
                        "rol",
                        ""
                    ),

                    "activo": x.get(
                        "activo",
                        False
                    )
                }

                for x in data
            ]

            self.current_page = 1

            self.load_data()

            self.page_ref.update()

        except httpx.ConnectTimeout:

            await self.toast.show(
                self.page_ref,
                "No se pudo conectar con el servidor",
                "error"
            )

        except httpx.RequestError as ex:

            print(
                "ERROR CONEXION:",
                ex
            )

            await self.toast.show(
                self.page_ref,
                "Error de conexión con la API",
                "error"
            )

        except Exception as ex:

            print(
                "ERROR:",
                ex
            )

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )

    # =========================================================
    # CARGAR TABLA
    # =========================================================

    def load_data(self):

        self.table.rows.clear()

        datos = self.usuarios
     

        # ==========================
        # FILTRO TEXTO
        # ==========================

        texto = (
            self.txt_busqueda.value or ""
        ).strip().lower()

        if texto:

            datos = [

                item

                for item in datos
               

                if texto in item[
                    "usuario"
                ].lower()

                or texto in item[
                    "nombre"
                ].lower()

                or texto in item[
                    "apellido"
                ].lower()

                or texto in item[
                    "rol"
                ].lower()
            ]

        # ==========================
        # FILTRO ACTIVOS
        # ==========================

        if self.chk_activos.value:

            datos = [

                item

                for item in datos

                if item["activo"]
            ]

        # ==========================
        # PAGINACION
        # ==========================

        self.total_items = len(datos)

        inicio = (
            self.current_page - 1
        ) * self.page_size

        fin = (
            inicio + self.page_size
        )

        datos_pagina = datos[
            inicio:fin
        ]

        # ==========================
        # FILAS
        # ==========================

        for item in datos_pagina:

            estado = (
                "Activo"
                if item["activo"]
                else "Inactivo"
            )

            self.table.rows.append(

                ft.DataRow(

                    cells=[

                        ft.DataCell(

                            ft.Text(
                                item["usuario"],
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
                                item["apellido"],
                                size=11
                            )
                        ),

                        ft.DataCell(

                            ft.Text(
                                item["rol"],
                                size=11
                            )
                        ),

                        ft.DataCell(

                            ft.Text(
                                estado,
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
                                        item=item:
                                            self.page_ref.run_task(
                                                self.abrir_formulario,
                                                item
                                            )
                                    ),

                                    ft.IconButton(

                                        icon=(
                                            ft.Icons.BLOCK
                                            if item["activo"]
                                            else ft.Icons.CHECK
                                        ),

                                        icon_size=18,

                                        tooltip=(
                                            "Desactivar"
                                            if item["activo"]
                                            else "Activar"
                                        ),

                                        on_click=lambda e,
                                        item=item:
                                            self.page_ref.run_task(
                                                self.cambiar_estado,
                                                item
                                            )
                                    ),

                                    ft.IconButton(

                                        icon=ft.Icons.DELETE,

                                        icon_size=18,

                                        icon_color="red",

                                        tooltip="Eliminar",

                                        on_click=lambda e,
                                        item=item:
                                            self.page_ref.run_task(
                                                self.confirmar_eliminar,
                                                item
                                            )
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        # ==========================
        # TOTALES
        # ==========================

        self.lbl_total.value = (
            f"Total registros: "
            f"{self.total_items}"
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
            f"Página "
            f"{self.current_page} "
            f"de "
            f"{total_pages}"
        )

    # =========================================================
    # BUSCAR
    # =========================================================

    async def buscar(self, e=None):

        self.current_page = 1

        filtro = {
            "busqueda": self.txt_busqueda.value.strip(),
            "activo": self.chk_activos.value,
        }

        await self.listar(filtro)

        self.load_data()

        self.page_ref.update()

    # =========================================================
    # SIGUIENTE PAGINA
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
    # PAGINA ANTERIOR
    # =========================================================

    async def prev_page(self, e):

        if self.current_page > 1:

            self.current_page -= 1

            self.load_data()

            self.page_ref.update()

    # =========================================================
    # RELOAD
    # =========================================================

    async def reload_view(self):

        self.txt_busqueda.value = ""

        self.chk_activos.value = True

        self.current_page = 1

        self.table.rows.clear()

        self.lbl_total.value = (
            "Total registros: 0"
        )

        self.lbl_page.value = ""

        await self.listar()

        self.update()

    # =========================================================
    # ABRIR FORMULARIO
    # =========================================================

    async def abrir_formulario(
        self,
        item
    ):

        view = (
            self.page_ref
            .layout
            .views
            .get("crear_usuario")
        )

        if item is not None:

            view.set_mode(
                item["id"]
            )

        else:

            view.set_mode(0)

        self.page_ref.layout.change_view(
            "crear_usuario"
        )

    # =========================================================
    # CAMBIAR ESTADO
    # =========================================================

    async def cambiar_estado(
        self,
        item
    ):

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

        usuario_id = item["id"]

        url = (
            f"{settings.URL_BACKEND}"
            f"/usuarios/{usuario_id}/estado"
        )

        params = {
                    "activo":  not item["activo"]
                }
        try:

            async with httpx.AsyncClient() as client:

                response = await client.patch(
                    url,
                    headers=headers,
                    params=params
                )

            if response.status_code == 401:

                await self.toast.show(
                    self.page_ref,
                    "Token inválido o expirado",
                    "error"
                )

                return

            if response.status_code not in (
                200,
                204
            ):

                await self.toast.show(
                    self.page_ref,
                    f"Error API: "
                    f"{response.status_code}",
                    "error"
                )

                return

            await self.toast.show(
                self.page_ref,
                "Estado actualizado",
                "success"
            )

            await self.buscar()

        except Exception as ex:

            print(
                "ERROR:",
                ex
            )

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )

    # =========================================================
    # CONFIRMAR ELIMINAR
    # =========================================================

    async def confirmar_eliminar(
        self,
        item
    ):

        dialog = ft.AlertDialog(

            modal=True,

            title=ft.Text(
                "Confirmar eliminación"
            ),

            content=ft.Text(
                "¿Realmente desea eliminar "
                f"el usuario "
                f"'{item['usuario']}'?"
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

        def cerrar():

            dialog.open = False

            self.page_ref.update()

        async def ejecutar():

            dialog.open = False

            self.page_ref.update()

            await self.eliminar_usuario(
                item
            )

        def confirmar():

            self.page_ref.run_task(
                ejecutar
            )

        if dialog not in self.page_ref.overlay:

            self.page_ref.overlay.append(
                dialog
            )

        self.page_ref.dialog = dialog

        dialog.open = True

        self.page_ref.update()

    # =========================================================
    # ELIMINAR
    # =========================================================

    async def eliminar_usuario(
        self,
        item
    ):

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

        usuario_id = item["id"]

        url = (
            f"{settings.URL_BACKEND}"
            f"/usuarios/{usuario_id}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.delete(
                    url,
                    headers=headers
                )

            if response.status_code == 401:

                await self.toast.show(
                    self.page_ref,
                    "Token inválido o expirado",
                    "error"
                )

                return

            if response.status_code not in (
                200,
                204
            ):

                await self.toast.show(
                    self.page_ref,
                    f"Error API: "
                    f"{response.status_code}",
                    "error"
                )

                return

            await self.toast.show(
                self.page_ref,
                "Usuario eliminado correctamente",
                "success"
            )

            await self.listar()

        except Exception as ex:

            print(
                "ERROR:",
                ex
            )

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )

