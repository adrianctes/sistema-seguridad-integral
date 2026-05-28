import flet as ft

from views.legajos.gestion.legajo_sidebar_view import Sidebar
from views.legajos.gestion.editar_view import EditarLegajoView
from views.legajos.gestion.licencias_view import LicenciasView
from views.legajos.gestion.historia_laboral.historia_laboral_view import HistoriaLaboralView
from views.legajos.gestion.familiares_view import FamiliaresView
from views.legajos.gestion.sanciones_view import SancionesView
from views.legajos.gestion.notas_view import NotasView


class GestionLegajoLayout(ft.Container):

    def __init__(self, page):
        super().__init__()

        self.page_ref = page

        self.current_key = "editar"

        self.legajo_id = None

        # =========================
        # VIEWS
        # =========================

        self.views = {

            "editar": EditarLegajoView(page),

            "licencias": LicenciasView(page),

            "historia": HistoriaLaboralView(page),

            "familiares": FamiliaresView(page),

            "sanciones": SancionesView(page),

            "notas": NotasView(page)

        }

        # =========================
        # SIDEBAR
        # =========================

        self.sidebar = Sidebar(
            page,
            self.change_view
        )

        self.sidebar_view = self.sidebar.build()

        # =========================
        # MAIN
        # =========================

        self.main_container = ft.Container(
            expand=True,
            content=self.views["editar"]
        )

        self.content = self.build_layout()

    def build_layout(self):

        return ft.Row(

            expand=True,

            controls=[

                self.sidebar_view,

                self.main_container

            ]
        )

    def change_view(self, route):

        if route not in self.views:
            return

        self.current_key = route

        vista = self.views[route]

        self.main_container.content = vista

        self.page_ref.update()

        # =========================
        # LOAD OPCIONAL
        # =========================

        if hasattr(vista, "load"):

            self.page_ref.run_task(
                vista.load,
                self.legajo_id
            )

    async def load(self):

        self.sidebar.set_default_item()

        # abrir editar por defecto
        self.change_view("editar")