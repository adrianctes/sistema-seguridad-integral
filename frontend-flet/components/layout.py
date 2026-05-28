import flet as ft
from components.sidebar import Sidebar
from views.legajos.legajo_list_view import LegajosView
from views.dashboard.dashboard_view import DashboardView
from views.legajos.gestion.gestion_layout import GestionLegajoLayout
from views.legajos.legajo_crear_view import CrearLegajoView


class Layout:

    def __init__(self, page: ft.Page):
   

        self.page = page
       
       
        # =========================
        # SIDEBAR
        # =========================
        self.sidebar = Sidebar(
            page,
            self.change_view
        )

        # =========================
        # VIEWS
        # =========================

        self.views = {
            "dashboard" : DashboardView(page),
            "legajos": LegajosView(page),
            "crear_legajo": CrearLegajoView(page),
            "gestion_legajo": GestionLegajoLayout(page)

        }

        # =========================
        # CONTENT
        # =========================

        self.content = ft.Container(

            expand=True,

            padding=0,
            
            content=self.views["dashboard"]

        )

    def build(self):

        return ft.Row(

            expand=True,

            controls=[

                self.sidebar,

                self.content

            ]
        )

    def change_view(self, view_name):

        if view_name in self.views:

            vista = self.views[view_name]

            self.content.content = vista

            # =========================
            # HOOKS OPCIONALES
            # =========================

            if view_name == "dashboard":
                if hasattr(vista, "load"):
                    self.page.run_task(
                        vista.load
                )    
               

            elif view_name == "legajos":

                if hasattr(vista, "listar_legajos"):

                    self.page.run_task(
                        vista.listar_legajos
                    )

            elif view_name in [
                "crear_legajo",
                "gestion_legajo"
            ]:

                if hasattr(vista, "load"):

                    self.page.run_task(
                        vista.load
                    )

        else:

            self.content.content = ft.Container(

                content=ft.Text(
                    f"Vista '{view_name}' en construcción",
                    size=26
                )
            )

        self.page.update()
