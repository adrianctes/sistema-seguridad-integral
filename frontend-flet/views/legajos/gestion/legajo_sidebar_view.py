import flet as ft


class Sidebar:

    def __init__(self, page, change_page):

        self.page = page
        self.change_page = change_page

        # COLORS
        self.bg = "#FFFFFF"
        self.text = "#111827"

        # hover
        self.hover = "#E5E7EB"

        # selected
        self.active_bg = "#769AE4"
        self.active_text = "RED"

        # selected item
        self.active_item = None

    # =========================
    # SELECT ITEM
    # =========================
    def select_item(self, e, route):

        # limpiar anterior
        if self.active_item:

            self.active_item.indicator.bgcolor = "transparent"

            self.active_item.label.color = self.text

            self.active_item.label.weight = ft.FontWeight.W_500

            self.active_item.update()

        # nuevo activo
        e.control.indicator.bgcolor = "red"

        e.control.label.color = "red"

        e.control.label.weight = ft.FontWeight.BOLD

        self.active_item = e.control

        e.control.update()

        # cambiar vista
        self.change_page(route)
    # =========================
    # HOVER
    # =========================
    def on_hover(self, e):

        # si es el activo no hacer hover
        if e.control == self.active_item:
            return

        if e.data == "true":

            e.control.bgcolor = self.hover

        else:

            e.control.bgcolor = self.bg

        e.control.update()

    # =========================
    # ITEM
    # =========================
    def item(self, text, route=None):

        indicator = ft.Container(
            width=4,
            height=22,
            bgcolor="transparent",
            border_radius=10
        )

        label = ft.Text(
            text,
            size=13,
            color=self.text,
            weight=ft.FontWeight.W_500
        )

        row = ft.Row(
            controls=[
                label,
                indicator
            ],
            alignment="spaceBetween",
            vertical_alignment="center"
        )

        container = ft.Container(

            height=38,

            padding=ft.Padding.only(
                left=12,
                right=8
            ),

            alignment=ft.Alignment(-1, 0),

            bgcolor=self.bg,

            ink=True,

            on_hover=lambda e: self.on_hover(e),

            content=row
        )

        # guardar referencias
        container.label = label
        container.indicator = indicator

        # click
        container.on_click = lambda e: self.select_item(
            e,
            route
        )

        return container
    # =========================
    # DIVIDER
    # =========================
    def divider(self):

        return ft.Container(
            height=1,
            border_radius=10,
            bgcolor="#111827",
            margin=ft.Margin(
                top=10,
                bottom=10,
                left=0,
                right=0
            )
        )

    # =========================
    # BUILD
    # =========================
    def build(self):

        self.editar_item = self.item(
            "Editar",
            "editar"
        )

        return ft.Container(
            width=170,
            bgcolor=self.bg,
            padding=ft.Padding.only(
                top=15,
                left=10,
                right=10,
                bottom=10
            ),
            content=ft.Column(
                spacing=5,
                controls=[

                    ft.Container(
                        padding=10,
                        content=ft.Text(
                            "Gestion\nLegajo",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="BLACK",
                        )
                    ),

                    self.divider(),

                    self.editar_item,

                    self.item("Familiares", "familiares"),

                    self.item("Licencias", "licencias"),

                    self.item("Sanciones", "sanciones"),

                    self.item("Historia laboral", "historia"),
                    
                    self.item("Notas", "notas"),
                ]
            )
        )
    def set_default_item(self):

        # limpiar activo anterior
        if self.active_item:

            self.active_item.indicator.bgcolor = "transparent"

            self.active_item.label.color = self.text

            self.active_item.label.weight = ft.FontWeight.W_500

        # activar editar
        self.active_item = self.editar_item

        self.editar_item.indicator.bgcolor = "red"

        self.editar_item.label.color = "red"

        self.editar_item.label.weight = ft.FontWeight.BOLD


   