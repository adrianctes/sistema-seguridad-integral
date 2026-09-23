
import flet as ft
from utils.permisos import tiene_permiso


class Sidebar(ft.Container):

    def __init__(self, page, on_logout, change_page):

        super().__init__()

        self.page_ref = page
        self.on_logout = on_logout
        self.change_page = change_page

        self.active = "dashboard"

        # =========================================================
        # PALETA
        # =========================================================

        self.bg = "#040B1C"
        self.active_bg = "#2B1625"
        self.active_color = "#FF6B6B"

        self.icon_color = "#8E9AB8"
        self.text_color = "#8E9AB8"

        self.active_text = "#FFFFFF"

        self.divider = "#111827"

        self.usuario_id = None
        self.ayn_usuario = None

        self.build()

    # =========================================================
    # ACTIVAR MENU
    # =========================================================

    def set_active(self, route):

        self.active = route

        self.build()

        self.update()

    # =========================================================
    # SELECCIONAR MENU
    # =========================================================

    def seleccionar_menu(self, e, route):

        self.set_active(route)

        if route == "cambiar_contrasena":

            self.change_page(
                route,
                self.usuario_id,
                self.ayn_usuario
            )

        else:

            self.change_page(route)

    # =========================================================
    # ITEM MENU
    # =========================================================

    def menu_item(
        self,
        icon,
        title,
        route,
        permiso_ACCEDER=None
    ):

        # -----------------------------------------
        # VALIDAR PERMISO
        # -----------------------------------------

        if permiso_ACCEDER is not None:

            if not tiene_permiso(
                self.page_ref,
                permiso_ACCEDER
            ):
                return None 

        active = self.active == route

        return ft.Container(

            height=50,

            border_radius=10,

            bgcolor=(
                self.active_bg
                if active
                else None
            ),

            padding=ft.Padding.symmetric(
                horizontal=8
            ),

            ink=True,

            animate=ft.Animation(
                180,
                ft.AnimationCurve.EASE_IN_OUT
            ),

            on_click=lambda e: self.seleccionar_menu(
                e,
                route
            ),

            content=ft.Row(

                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                controls=[

                    ft.Row(

                        spacing=14,

                        controls=[

                            ft.Icon(
                                icon,
                                size=20,
                                color=(
                                    self.active_color
                                    if active
                                    else self.icon_color
                                )
                            ),

                            ft.Text(
                                title,
                                size=14,

                                color=(
                                    self.active_text
                                    if active
                                    else self.text_color
                                ),

                                weight=(
                                    ft.FontWeight.BOLD
                                    if active
                                    else ft.FontWeight.W_500
                                )
                            )
                        ]
                    ),

                    ft.Container(

                        width=4,
                        height=26,

                        border_radius=20,

                        bgcolor=(
                            self.active_color
                            if active
                            else None
                        )
                    )
                ]
            )
        )

    # =========================================================
    # BUILD
    # =========================================================

    def build(self):

        # =====================================================
        # USUARIO
        # =====================================================

        usuario = (
            self.page_ref.session.store.get("usuario")
            or {}
        )

        self.usuario_id = usuario.get(
            "id",
            0
        )

        nombre = usuario.get(
            "nombre",
            ""
        )

        apellido = usuario.get(
            "apellido",
            ""
        )

        self.ayn_usuario = (
            f"{apellido} {nombre}"
        )

        rol = usuario.get(
            "rol",
            ""
        )

        # =====================================================
        # SIDEBAR
        # =====================================================

        self.width = 245

        self.bgcolor = self.bg

        self.padding = ft.Padding.only(
            top=12,
            left=0,
            right=8,
            bottom=18
        )

        self.border = ft.Border(
            right=ft.BorderSide(
                1,
                self.divider
            )
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = ft.Container(

            height=60,

            padding=ft.Padding.only(
                left=8,
                right=8
            ),

            content=ft.Row(

                spacing=12,

                vertical_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                controls=[

                    ft.Container(

                        width=34,
                        height=34,

                        border_radius=8,

                        bgcolor="#FFFFFF10",

                        alignment=ft.Alignment.CENTER,

                        content=ft.Icon(
                            ft.Icons.SHIELD_OUTLINED,
                            color="white",
                            size=20
                        )
                    ),

                    ft.Text(
                        "SAP Seguridad",

                        size=20,

                        weight=ft.FontWeight.BOLD,

                        color="white"
                    )
                ]
            )
        )

        # =====================================================
        # LEGAJOS
        # =====================================================

        legajos = self.menu_item(

            ft.Icons.BADGE_OUTLINED,

            "Legajos",

            "legajos",

            "LEGAJOS_ACCEDER"
        )

        # =====================================================
        # LIQUIDACION
        # =====================================================

        liquidacion_items = [

            self.menu_item(
                ft.Icons.SETTINGS_OUTLINED,
                "Datos fijos",
                "datos_fijos_liquidacion",
                "SUELDOS_LIQUIDACION_DATOS_FIJOS_ACCEDER"  
            ),

            self.menu_item(
                ft.Icons.CALCULATE_OUTLINED,
                "Liquidaciones",
                "liquidacion_haberes",
                "SUELDOS_LIQUIDACION_LIQUIDACIONES_ACCEDER"
            ),
        ]

        liquidacion_items = [
            item
            for item in liquidacion_items
            if item is not None
        ]

        liquidacion = None

        permisos_sueldos = [
                    "SUELDOS_LIQUIDACION_LIQUIDACIONES_ACCEDER",
                    "SUELDOS_LIQUIDACION_DATOS_FIJOS_ACCEDER"
                ]
        
        tiene_acceso_sueldos = any(
            tiene_permiso(self.page_ref, permiso)
            for permiso in permisos_sueldos
        )
        
        if tiene_acceso_sueldos:
            # agregar menú SUELDOS

            liquidacion = ft.ExpansionTile(

                leading=ft.Icon(
                    ft.Icons.RECEIPT_LONG_ROUNDED,
                    color=self.icon_color,
                    size=20
                ),

                title=ft.Text(
                    "Liquidación",
                    size=14,
                    color=self.text_color,
                    weight=ft.FontWeight.W_500
                ),

                tile_padding=ft.Padding.only(
                    left=16,
                    right=16
                ),

                controls_padding=ft.Padding.only(
                    left=16
                ),

                collapsed_icon_color=self.icon_color,

                icon_color=self.icon_color,

                controls=liquidacion_items
            )

        # =====================================================
        # SUELDOS
        # =====================================================

        sueldos_items = []
            
        if liquidacion is not None:
               sueldos_items.append(
                    liquidacion
                )


        if tiene_permiso(
                self.page_ref,
                "SUELDOS_CONCEPTOS_ACCEDER"
            ):

                item = self.menu_item(

                    ft.Icons.CALCULATE_OUTLINED,

                    "Conceptos",

                    "conceptos",

                    "SUELDOS_CONCEPTOS_ACCEDER"
                )

                if item is not None:
                    sueldos_items.append(item)


        if tiene_permiso(
                self.page_ref,
                "SUELDOS_NOVEDADES_ACCEDER"
            ):

                item = self.menu_item(

                    ft.Icons.EDIT_NOTE_ROUNDED,

                    "Novedades",

                    "novedades",

                    "SUELDOS_NOVEDADES_ACCEDER"
                )

                if item is not None:
                    sueldos_items.append(item)

        # -----------------------------------------
        # CREAR SUELDOS SOLO SI TIENE PERMISO
        # -----------------------------------------

        sueldos = None

        permisos_sueldos = [
            "SUELDOS_LIQUIDACION_LIQUIDACIONES_ACCEDER",
            "SUELDOS_NOVEDADES_ACCEDER",
            "SUELDOS_CONCEPTOS_ACCEDER",
        ]

        tiene_acceso_sueldos = any(
            tiene_permiso(self.page_ref, permiso)
            for permiso in permisos_sueldos
        )

        if tiene_acceso_sueldos:
            # agregar menú SUELDOS

            sueldos_items = [
                item
                for item in sueldos_items
                if item is not None
                ]

            if sueldos_items:

                    sueldos = ft.Container(

                        border_radius=10,

                        bgcolor="#091224",

                        padding=ft.Padding.only(
                            top=4,
                            bottom=4
                        ),

                        content=ft.ExpansionTile(

                            title=ft.Text(
                                "Sueldos",

                                size=14,

                                color=self.text_color,

                                weight=ft.FontWeight.W_500
                            ),

                            leading=ft.Icon(
                                ft.Icons.ATTACH_MONEY_ROUNDED,
                                color=self.icon_color,
                                size=20
                            ),

                            collapsed_text_color=self.text_color,

                            text_color="white",

                            icon_color=self.icon_color,

                            collapsed_icon_color=self.icon_color,

                            tile_padding=ft.Padding.symmetric(
                                horizontal=16
                            ),

                            controls_padding=ft.Padding.only(
                                left=12,
                                right=0,
                                bottom=6
                            ),

                            controls=sueldos_items
                        )
                    )

        # =====================================================
        # USUARIOS
        # =====================================================

        usuarios_items = [

            self.menu_item(
                ft.Icons.MANAGE_ACCOUNTS_ROUNDED,
                "Gestionar usuarios",
                "gestionar_usuarios",
                "USUARIOS_GESTIONAR_USUARIOS_ACCEDER"
            ),

            self.menu_item(
                ft.Icons.LOCK_RESET_ROUNDED,
                "Permisos",
                "permiso_usuario",
                "USUARIOS_PERMISOS_ACCEDER"
            ),

            self.menu_item(
                ft.Icons.LOCK_RESET_ROUNDED,
                "Cambiar contraseña",
                "cambiar_contrasena"
            ),
        ]

        usuarios_items = [
            item
            for item in usuarios_items
            if item is not None
        ]

        usuarios = None
        print(len(usuarios_items))

        usuarios = ft.ExpansionTile(

                leading=ft.Icon(
                    ft.Icons.PERSON_OUTLINE_ROUNDED,
                    color=self.icon_color,
                    size=20
                ),

                title=ft.Text(
                    "Usuarios",
                    size=14,
                    color=self.text_color,
                    weight=ft.FontWeight.W_500
                ),

                tile_padding=ft.Padding.only(
                    left=16,
                    right=16
                ),

                controls_padding=ft.Padding.only(
                    left=16
                ),

                collapsed_icon_color=self.icon_color,

                icon_color=self.icon_color,

                controls=usuarios_items
            )

        # =====================================================
        # AUDITORIA
        # =====================================================

        auditoria_items = [

            self.menu_item(
                ft.Icons.LIST_ALT_ROUNDED,
                "Registro de actividades",
                "registro_actividades",
                "SEGURIDAD_AUDITORIA_ACCEDER"
            )
        ]

        auditoria_items = [
            item
            for item in auditoria_items
            if item is not None
        ]

        auditoria = None

        if auditoria_items:

            auditoria = ft.ExpansionTile(

                leading=ft.Icon(
                    ft.Icons.HISTORY_ROUNDED,
                    color=self.icon_color,
                    size=20
                ),

                title=ft.Text(
                    "Auditoría",
                    size=14,
                    color=self.text_color,
                    weight=ft.FontWeight.W_500
                ),

                tile_padding=ft.Padding.only(
                    left=16,
                    right=16
                ),

                controls_padding=ft.Padding.only(
                    left=16
                ),

                collapsed_icon_color=self.icon_color,

                icon_color=self.icon_color,

                controls=auditoria_items
            )

        # =====================================================
        # SEGURIDAD
        # =====================================================

        seguridad = None

       

        seguridad_items = []

        if usuarios is not None:

                seguridad_items.append(
                    usuarios
                )

        if auditoria is not None:

                seguridad_items.append(
                    auditoria
                )

            # -----------------------------------------
            # CREAR SEGURIDAD SOLO SI TIENE CONTENIDO
            # -----------------------------------------

        if seguridad_items:

                seguridad = ft.Container(

                    border_radius=10,

                    content=ft.ExpansionTile(

                        title=ft.Text(
                            "Seguridad",

                            size=14,

                            color=self.text_color,

                            weight=ft.FontWeight.W_500
                        ),

                        leading=ft.Icon(
                            ft.Icons.SECURITY_ROUNDED,
                            color=self.icon_color,
                            size=20
                        ),

                        collapsed_text_color=self.text_color,

                        text_color="white",

                        icon_color=self.icon_color,

                        collapsed_icon_color=self.icon_color,

                        tile_padding=ft.Padding.symmetric(
                            horizontal=16
                        ),

                        controls_padding=ft.Padding.only(
                            left=12,
                            right=0,
                            bottom=6
                        ),

                        controls=seguridad_items
                    )
                )

        # =====================================================
        # CONTROLES DEL MENU
        # =====================================================

        menu_items = [

            legajos,

            sueldos,

            seguridad
        ]

        menu_items = [
            item
            for item in menu_items
            if item is not None
        ]

        # =====================================================
        # MENU
        # SOLO ESTA PARTE TIENE SCROLL
        # =====================================================

        menu = ft.Container(

            expand=True,

            padding=ft.Padding.only(
                top=6,
                bottom=6
            ),

            content=ft.Column(

                spacing=4,

                scroll=ft.ScrollMode.AUTO,

                controls=menu_items
            )
        )

        # =====================================================
        # FOOTER
        # =====================================================

        footer = ft.Container(

            padding=ft.Padding.only(
                left=8,
                right=8,
                top=10,
                bottom=8
            ),

            content=ft.Column(

                spacing=10,

                controls=[

                    # -----------------------------------------
                    # USUARIO
                    # -----------------------------------------

                    ft.Row(

                        spacing=10,

                        controls=[

                            ft.Container(

                                width=38,
                                height=38,

                                border_radius=20,

                                bgcolor="#FFFFFF10",

                                alignment=ft.Alignment.CENTER,

                                content=ft.Text(

                                    (
                                        nombre[:1]
                                        + apellido[:1]
                                    ).upper(),

                                    size=13,

                                    weight=ft.FontWeight.BOLD,

                                    color="white"
                                )
                            ),

                            ft.Column(

                                spacing=2,

                                expand=True,

                                controls=[

                                    ft.Text(

                                        f"{nombre} {apellido}",

                                        size=13,

                                        weight=ft.FontWeight.BOLD,

                                        color="white",

                                        max_lines=1,

                                        overflow=(
                                            ft.TextOverflow.ELLIPSIS
                                        )
                                    ),

                                    ft.Text(

                                        rol,

                                        size=11,

                                        color=self.text_color,

                                        max_lines=1,

                                        overflow=(
                                            ft.TextOverflow.ELLIPSIS
                                        )
                                    )
                                ]
                            )
                        ]
                    ),

                    # -----------------------------------------
                    # CERRAR SESION
                    # -----------------------------------------

                    ft.Container(

                        height=45,

                        border_radius=10,

                        padding=ft.Padding.symmetric(
                            horizontal=8
                        ),

                        ink=True,

                        on_click=self.cerrar_sesion,

                        content=ft.Row(

                            spacing=12,

                            controls=[

                                ft.Icon(
                                    ft.Icons.LOGOUT_ROUNDED,
                                    size=20,
                                    color=self.icon_color
                                ),

                                ft.Text(
                                    "Cerrar sesión",
                                    size=14,
                                    color=self.text_color
                                )
                            ]
                        )
                    )
                ]
            )
        )

        # =====================================================
        # CONTENIDO FINAL
        # =====================================================

        self.content = ft.Column(

            expand=True,

            spacing=0,

            controls=[

                # HEADER

                header,

                # DIVISOR

                ft.Divider(
                    color=self.divider,
                    height=1
                ),

                # MENU

                menu,

                # DIVISOR

                ft.Divider(
                    color=self.divider,
                    height=1
                ),

                # FOOTER

                footer
            ]
        )

    # =========================================================
    # CERRAR SESION
    # =========================================================

    async def cerrar_sesion(self, e):

        # -----------------------------------------
        # TOKEN
        # -----------------------------------------

        if (
            self.page.session.store.get(
                "access_token"
            ) is not None
        ):

            self.page.session.store.remove(
                "access_token"
            )

        # -----------------------------------------
        # USUARIO
        # -----------------------------------------

        if (
            self.page.session.store.get(
                "usuario"
            ) is not None
        ):

            self.page.session.store.remove(
                "usuario"
            )

        # -----------------------------------------
        # LOGIN
        # -----------------------------------------

        self.on_logout()