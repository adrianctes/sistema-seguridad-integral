import flet as ft


class Sidebar(ft.Container):

    def __init__(self, page, on_logout, change_page):

        super().__init__()

        self.page_ref = page
        self.on_logout = on_logout
        self.change_page = change_page

        self.active = "legajos"# "dashboard"

        # PALETA
        self.bg = "#040B1C"
        self.active_bg = "#2B1625"
        self.active_color = "#FF6B6B"

        self.icon_color = "#8E9AB8"
        self.text_color = "#8E9AB8"

        self.active_text = "#FFFFFF"

        self.divider = "#111827"

        self.build()

    def set_active(self, route):

        self.active = route

        self.change_page(route)

        self.build()

        self.update()

    def menu_item(self, icon, title, route):

        active = self.active == route

        return ft.Container(

            height=56,

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

            on_click=lambda e: self.set_active(route),

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

    def build(self):

        usuario = self.page_ref.session.store.get("usuario") or {}
        nombre = usuario.get("nombre", "")
        apellido = usuario.get("apellido", "")
        rol = usuario.get("rol", "")


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

        self.content = ft.Column(

            expand=True,

            spacing=6,

            controls=[

                # HEADER

                ft.Container(

                    padding=ft.Padding.only(
                        left=8,
                        top=10,
                        bottom=22
                    ),

                    content=ft.Row(

                        spacing=12,

                        controls=[

                            ft.Container(

                                width=34,
                                height=34,

                                border_radius=8,

                                bgcolor="#FFFFFF10",

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
                ),

                ft.Divider(
                    color=self.divider,
                    height=1
                ),

                # MENU

                

                self.menu_item(
                    ft.Icons.BADGE_OUTLINED,
                    "Legajos",
                    "legajos"
                ),

                # GESTION DE HABERES

                ft.Container(

                    border_radius=10,

                    bgcolor="#091224",

                    padding=ft.Padding.only(
                        left =0,
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

                        controls=[

                            ft.ExpansionTile(

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

                                        controls=[

                                            self.menu_item(
                                                ft.Icons.SETTINGS_OUTLINED,
                                                "Datos fijos",
                                                "datos_fijos_liquidacion"
                                            ),

                                            self.menu_item(
                                                ft.Icons.CALCULATE_OUTLINED,
                                                "Haberes",
                                                "liquidacion_haberes"
                                            ),          

                                           
                                        ],
                                    ),

                            self.menu_item(
                                ft.Icons.CALCULATE_OUTLINED,
                                "Conceptos",
                                "conceptos"
                            ),

                            self.menu_item(
                                ft.Icons.EDIT_NOTE_ROUNDED,
                                "Novedades",
                                "novedades"
                            ),

                            

                        ]
                    )
                ),

      
                ft.Container(
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
                            controls=[
                                ft.ExpansionTile(
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
                                    controls=[
                                      
                                        self.menu_item(
                                            ft.Icons.MANAGE_ACCOUNTS_ROUNDED,
                                            "Gestionar usuarios",
                                            "gestionar_usuarios"
                                        ),
                                        
                                        self.menu_item(
                                            ft.Icons.LOCK_RESET_ROUNDED,
                                            "Cambiar contraseña",
                                            "cambiar_contrasena"
                                        ),
                                    ],
                                ),
                                ft.ExpansionTile(
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
                                    controls=[
                                        self.menu_item(
                                            ft.Icons.LIST_ALT_ROUNDED,
                                            "Registro de actividades",
                                            "registro_actividades"
                                        )
                                    ],
                                ),
                            ]
                        ),
                        
                    ),
                                                
                ft.Container(expand=True),

                ft.Divider(
                    color=self.divider,
                    height=1
                ),

                # FOOTER

                 ft.Container(
    padding=ft.Padding.only(
        left=8,
        right=8,
        top=10,
        bottom=8
    ),
    content=ft.Column(
        spacing=10,
        controls=[
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
                                nombre[:1] + apellido[:1]
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
                                overflow=ft.TextOverflow.ELLIPSIS
                            ),

                            ft.Text(
                                rol,
                                size=11,
                                color=self.text_color,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS
                            )
                        ]
                    )
                ]
            ),

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
            ]
        ) 

    async def cerrar_sesion(self, e):
        # Eliminar datos de la sesión
        if self.page.session.store.get("access_token") is not None:
            self.page.session.store.remove("access_token")
            self.page.session.store.remove("usuario")

        # Volver al login
        self.on_logout()
