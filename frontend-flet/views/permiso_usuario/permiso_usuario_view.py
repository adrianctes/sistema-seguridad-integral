import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings


class PermisoUsuarioView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page

        self.toast = Toast()

        self.permisos = []

        self.permisos_seleccionados = set()

        self.rol = "OPERADOR"

        # =====================================================
        # ESTILO GENERAL
        # =====================================================

        self.expand = True

        self.bgcolor = "#F1F5F9"

        self.padding = 20

        # =====================================================
        # DROPDOWN ROLES
        # =====================================================

        self.dropdown_rol = ft.Dropdown(

            label="Rol",

            value=self.rol,

            width=300,

            height=55,

            options=[],

            text_size=12,

            label_style=ft.TextStyle(
                size=11,
                color="#64748B"
            ),

            border_color="#CBD5E1",

            focused_border_color="#030B16",

            bgcolor="white",

            border_radius=4,

            content_padding=10,
            on_select=self.cambiar_rol
        )

        # =====================================================
        # BOTON GUARDAR
        # =====================================================

        self.btn_guardar = ft.FilledButton(

            "Guardar",

            icon=ft.Icons.SAVE,

            width=130,

            height=36,

            style=ft.ButtonStyle(

                shape=ft.RoundedRectangleBorder(
                    radius=0
                ),

                bgcolor="#030B16",

                color="white"
            ),

            on_click=lambda e:
                self.page_ref.run_task(
                    self.guardar
                )
        )

        # =====================================================
        # LOADING
        # =====================================================

        self.loading = ft.ProgressRing(

            visible=False,

            width=20,

            height=20
        )

        # =====================================================
        # GRILLA PRINCIPAL
        # =====================================================

        self.grilla = ft.Column(

            spacing=0,

            scroll=ft.ScrollMode.AUTO,

            expand=True
        )

        # =====================================================
        # GRILLA ACCIONES ESPECIALES
        # =====================================================

        self.grilla_acciones_especiales = ft.Column(

            spacing=0,

            scroll=ft.ScrollMode.AUTO,

            expand=True
        )

        # =====================================================
        # CONTENIDO
        # =====================================================

        contenido = ft.Column(

            expand=True,

            spacing=10,

            controls=[

                # =================================================
                # HEADER
                # =================================================

                ft.Row(

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                    controls=[

                        ft.Column(

                            spacing=1,

                            controls=[

                                ft.Text(

                                    "Permisos",

                                    size=18,

                                    weight=ft.FontWeight.BOLD,

                                    color="#0F172A"
                                ),

                                ft.Text(

                                    "Administración de permisos por rol",

                                    size=11,

                                    color="#64748B"
                                )
                            ]
                        )
                    ]
                ),

                # =================================================
                # CONFIGURACION DEL ROL
                # =================================================

                ft.Container(

                    height=76,

                    bgcolor="white",

                    padding=10,

                    border=ft.Border.all(
                        1,
                        "#E2E8F0"
                    ),

                    content=ft.Row(

                        vertical_alignment=(
                            ft.CrossAxisAlignment.CENTER
                        ),

                        controls=[

                            ft.Column(

                                width=300,

                                spacing=0,

                                controls=[

                                    ft.Text(
                                        size=10,
                                        color="#64748B"
                                    ),

                                    self.dropdown_rol
                                ]
                            ),

                            ft.Container(
                                expand=True
                            ),

                            self.btn_guardar,

                            self.loading
                        ]
                    )
                ),

                # =================================================
                # PERMISOS PRINCIPALES
                # =================================================

                ft.Container(

                    expand=True,

                    bgcolor="white",

                    border=ft.Border.all(
                        1,
                        "#E2E8F0"
                    ),

                    padding=10,

                    content=ft.Column(

                        expand=True,

                        spacing=8,

                        controls=[

                            # -------------------------------------
                            # TITULO
                            # -------------------------------------

                            ft.Row(

                                alignment=(
                                    ft.MainAxisAlignment
                                    .SPACE_BETWEEN
                                ),

                                controls=[

                                    ft.Text(

                                        "Permisos",

                                        size=13,

                                        weight=(
                                            ft.FontWeight.BOLD
                                        ),

                                        color="#0F172A"
                                    ),

                                    ft.Text(

                                        "Seleccione las operaciones permitidas",

                                        size=11,

                                        color="#64748B"
                                    )
                                ]
                            ),

                            ft.Divider(
                                height=1
                            ),

                            # -------------------------------------
                            # GRILLA
                            # -------------------------------------

                            ft.Container(

                                expand=True,

                                content=self.grilla
                            )
                        ]
                    )
                )
            ]
        )

        # =====================================================
        # STACK
        # =====================================================

        self.content = ft.Stack(

            expand=True,

            controls=[

                contenido,

                self.toast
            ]
        )

    # =========================================================
    # LOAD
    # =========================================================

    async def load(self):

        self.loading.visible = True

        self.grilla.controls.clear()

        self.page_ref.update()

        try:

            token = self.page_ref.session.store.get(
                "access_token"
            )

            # -------------------------------------------------
            # 1. TODOS LOS PERMISOS
            # -------------------------------------------------

            self.permisos = await (
                self.listar_permisos(
                    token
                )
            )

            # -------------------------------------------------
            # 2. ROLES
            # -------------------------------------------------

            await self.cargar_roles()

            # -------------------------------------------------
            # 3. PERMISOS DEL ROL
            # -------------------------------------------------

            await self.cargar_permisos_rol()

            # -------------------------------------------------
            # 4. GRILLA
            # -------------------------------------------------

            self.construir_grilla()

            self.page_ref.update()

        except Exception as e:

            print(
                "ERROR LOAD:",
                e
            )

            await self.toast.show(
                self.page_ref,
                f"Error cargando autorizaciones: {e}",
                "error"
            )

        finally:

            self.loading.visible = False

            self.page_ref.update()

    # =========================================================
    # OBTENER ROLES
    # =========================================================

    async def obtener_roles(self):

        token = self.page_ref.session.store.get(
            "access_token"
        )

        async with httpx.AsyncClient() as client:

            response = await client.get(

                f"{settings.URL_BACKEND}/roles",

                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            response.raise_for_status()

            return response.json()

    # =========================================================
    # CARGAR ROLES
    # =========================================================

    async def cargar_roles(self):

        try:

            data = await self.obtener_roles()

            self.dropdown_rol.options = [

                ft.DropdownOption(

                    key=rol["key"],

                    text=rol["text"]
                )

                for rol in data
            ]

            # -------------------------------------------------
            # SELECCIONAR PRIMER ROL
            # -------------------------------------------------

            if data:

                self.rol = data[0]["key"]

                self.dropdown_rol.value = self.rol

            self.page_ref.update()

        except Exception as e:

            print(
                "ERROR CARGANDO ROLES:",
                e
            )

            await self.toast.show(
                self.page_ref,
                f"Error cargando roles: {e}",
                "error"
            )

    # =========================================================
    # CAMBIAR ROL
    # =========================================================

    def cambiar_rol(self, e):
        print(self.rol)
        self.rol = e.control.value

        self.page_ref.run_task(
            self.cargar_permisos_rol
        )

    # =========================================================
    # OBTENER PERMISOS DEL ROL
    # =========================================================

    async def obtener_permisos_rol(
        self,
        token,
        rol
    ):

        async with httpx.AsyncClient() as client:

            response = await client.get(

                f"{settings.URL_BACKEND}/permisos/roles/{rol}",

                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            response.raise_for_status()

            return response.json()

    # =========================================================
    # CARGAR PERMISOS DEL ROL
    # =========================================================

    async def cargar_permisos_rol(self):

        try:

            token = self.page_ref.session.store.get(
                "access_token"
            )

            data = await self.obtener_permisos_rol(
                token,
                self.rol
            )

            self.permisos_seleccionados = set(

                data.get(
                    "permisos_ids",
                    []
                )
            )

            print(
                "PERMISOS SELECCIONADOS:",
                self.permisos_seleccionados
            )

            self.construir_grilla()

            self.grilla.update()

        except Exception as e:

            print(
                "ERROR CARGANDO PERMISOS DEL ROL:",
                e
            )

            await self.toast.show(
                self.page_ref,
                f"Error cargando permisos del rol: {e}",
                "error"
            )

    # =========================================================
    # CONSTRUIR GRILLA
    # =========================================================

    def construir_grilla(self):

        self.grilla.controls.clear()

        permisos_por_modulo = {}

        permisos_especiales = []

        acciones_principales = [

            "VER",
            "CREAR",
            "EDITAR",
            "ELIMINAR"
        ]

        # =====================================================
        # SEPARAR PERMISOS
        # =====================================================

        for permiso in self.permisos:

            accion = permiso["accion"]

            if accion in acciones_principales:

                modulo = permiso["modulo"]

                permisos_por_modulo.setdefault(
                    modulo,
                    []
                ).append(
                    permiso
                )

            else:

                permisos_especiales.append(
                    permiso
                )

        # =====================================================
        # CABECERA
        # =====================================================

        self.grilla.controls.append(

            self._crear_cabecera()
        )

        # =====================================================
        # MODULOS
        # =====================================================

        for modulo, permisos in (
            permisos_por_modulo.items()
        ):

            self.grilla.controls.append(

                self._crear_fila_modulo(
                    modulo,
                    permisos
                )
            )

        # =====================================================
        # ACCIONES ESPECIALES
        # =====================================================

        if permisos_especiales:

            self.grilla.controls.append(

                ft.Container(
                    height=15
                )
            )

            self.grilla.controls.append(

                self._crear_separador_especiales()
            )

            # -------------------------------------------------
            # LIMPIAR
            # -------------------------------------------------

            self.grilla_acciones_especiales.controls.clear()

            # -------------------------------------------------
            # AGREGAR
            # -------------------------------------------------

            for permiso in permisos_especiales:

                self.grilla_acciones_especiales.controls.append(

                    self._crear_fila_especial(
                        permiso
                    )
                )

            # -------------------------------------------------
            # CONTENEDOR
            # -------------------------------------------------

            self.grilla.controls.append(

                ft.Container(

                    height=220,

                    bgcolor="white",

                    border=ft.Border.all(
                        1,
                        "#E2E8F0"
                    ),

                    content=ft.Column(

                        expand=True,

                        controls=[

                            self.grilla_acciones_especiales
                        ]
                    )
                )
            )

    # =========================================================
    # CABECERA
    # =========================================================

    def _crear_cabecera(self):

        controles = [

            ft.Container(

                width=220,

                height=36,

                padding=ft.Padding.symmetric(
                    horizontal=10
                ),

                alignment=ft.Alignment.CENTER_LEFT,

                content=ft.Text(

                    "MÓDULO",

                    size=11,

                    weight=ft.FontWeight.BOLD,

                    color="#0F172A"
                )
            )
        ]

        for accion in [

            "VER",
            "CREAR",
            "EDITAR",
            "ELIMINAR"

        ]:

            controles.append(

                ft.Container(

                    width=90,

                    height=36,

                    alignment=ft.Alignment.CENTER,

                    content=ft.Text(

                        accion,

                        size=10,

                        weight=ft.FontWeight.BOLD,

                        color="#0F172A"
                    )
                )
            )

        return ft.Container(

            height=36,

            bgcolor="#E2E8F0",

            border=ft.Border.all(
                1,
                "#CBD5E1"
            ),

            content=ft.Row(

                controls=controles,

                spacing=0
            )
        )

    # =========================================================
    # FILA MODULO
    # =========================================================

    def _crear_fila_modulo(
        self,
        modulo,
        permisos
    ):

        permisos_dict = {

            permiso["accion"]: permiso

            for permiso in permisos
        }

        controles = [

            ft.Container(

                width=220,

                height=40,

                padding=ft.Padding.symmetric(
                    horizontal=10
                ),

                alignment=ft.Alignment.CENTER_LEFT,

                content=ft.Text(

                    modulo.capitalize(),

                    size=11,

                    weight=ft.FontWeight.W_500,

                    color="#0F172A"
                )
            )
        ]

        for accion in [

            "VER",
            "CREAR",
            "EDITAR",
            "ELIMINAR"

        ]:

            permiso = permisos_dict.get(
                accion
            )

            if permiso:

                checkbox = ft.Checkbox(

                    value=(

                        permiso["id"]

                        in self.permisos_seleccionados
                    ),

                    scale=0.85,

                    active_color="#030B16",

                    check_color="white",

                    on_change=lambda e,
                    permiso_id=permiso["id"]:

                    self.cambiar_permiso(

                        permiso_id,

                        e.control.value
                    )
                )

            else:

                checkbox = ft.Checkbox(

                    disabled=True,

                    scale=0.85
                )

            controles.append(

                ft.Container(

                    width=90,

                    height=40,

                    alignment=ft.Alignment.CENTER,

                    content=checkbox
                )
            )

        return ft.Container(

            height=40,

            bgcolor="white",

            border=ft.Border.only(

                bottom=ft.BorderSide(

                    1,

                    "#E2E8F0"
                )
            ),

            content=ft.Row(

                controls=controles,

                spacing=0
            )
        )

    # =========================================================
    # SEPARADOR ACCIONES ESPECIALES
    # =========================================================

    def _crear_separador_especiales(self):

        return ft.Container(

            height=36,

            bgcolor="#F8FAFC",

            padding=ft.Padding.symmetric(
                horizontal=10
            ),

            content=ft.Row(

                vertical_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                controls=[

                    ft.Icon(

                        ft.Icons.TUNE,

                        size=16,

                        color="#475569"
                    ),

                    ft.Text(

                        "ACCIONES ESPECIALES",

                        size=11,

                        weight=ft.FontWeight.BOLD,

                        color="#475569"
                    )
                ],

                spacing=7
            )
        )

    # =========================================================
    # FILA ACCION ESPECIAL
    # =========================================================

    def _crear_fila_especial(
        self,
        permiso
    ):

        checkbox = ft.Checkbox(

            value=(

                permiso["id"]

                in self.permisos_seleccionados
            ),

            scale=0.85,

            active_color="#030B16",

            check_color="white",

            on_change=lambda e,
            permiso_id=permiso["id"]:

            self.cambiar_permiso(

                permiso_id,

                e.control.value
            )
        )

        return ft.Container(

            height=40,

            padding=ft.Padding.symmetric(
                horizontal=10
            ),

            bgcolor="white",

            border=ft.Border.only(

                bottom=ft.BorderSide(

                    1,

                    "#E2E8F0"
                )
            ),

            content=ft.Row(

                vertical_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                controls=[

                    ft.Container(

                        expand=True,

                        content=ft.Text(

                            permiso["nombre"],

                            size=11,

                            color="#334155"
                        )
                    ),

                    ft.Container(

                        width=60,

                        alignment=ft.Alignment.CENTER,

                        content=checkbox
                    )
                ],

                spacing=0
            )
        )

    # =========================================================
    # CAMBIAR PERMISO
    # =========================================================

    def cambiar_permiso(
        self,
        permiso_id,
        seleccionado
    ):

        if seleccionado:

            self.permisos_seleccionados.add(
                permiso_id
            )

        else:

            self.permisos_seleccionados.discard(
                permiso_id
            )

    # =========================================================
    # GUARDAR
    # =========================================================

    async def guardar(
        self,
        e=None
    ):

        self.btn_guardar.disabled = True

        self.loading.visible = True

        self.page_ref.update()

        try:

            token = self.page_ref.session.store.get(
                "access_token"
            )

            await self.guardar_permisos_rol(

                token=token,

                rol=self.rol,

                permisos_ids=list(
                    self.permisos_seleccionados
                )
            )

            await self.toast.show(

                self.page_ref,

                "Permisos guardados correctamente",

                "success"
            )

        except Exception as e:

            print(
                "ERROR GUARDANDO:",
                e
            )

            await self.toast.show(

                self.page_ref,

                f"Error al guardar permisos: {e}",

                "error"
            )

        finally:

            self.btn_guardar.disabled = False

            self.loading.visible = False

            self.page_ref.update()

    # =========================================================
    # LISTAR PERMISOS
    # =========================================================

    async def listar_permisos(
        self,
        token
    ):

        async with httpx.AsyncClient() as client:

            response = await client.get(

                f"{settings.URL_BACKEND}/permisos",

                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            response.raise_for_status()

            return response.json()

    # =========================================================
    # GUARDAR PERMISOS DEL ROL
    # =========================================================

    async def guardar_permisos_rol(
        self,
        token,
        rol,
        permisos_ids
    ):

        async with httpx.AsyncClient() as client:

            response = await client.put(

                f"{settings.URL_BACKEND}/permisos/roles/{rol}",

                headers={
                    "Authorization": f"Bearer {token}"
                },

                json={
                    "permisos_ids": permisos_ids
                }
            )

            response.raise_for_status()

            return True
