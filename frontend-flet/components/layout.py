import flet as ft
from components.sidebar import Sidebar
from views.legajos.legajo_list_view import LegajosView
from views.dashboard.dashboard_view import DashboardView
from views.Gestion_haberes.novedades.novedades_view import NovedadesView
from views.legajos.gestion.gestion_layout import GestionLegajoLayout
from views.legajos.legajo_crear_view import CrearLegajoView
from views.Gestion_haberes.conceptos.concepto_list_view import ConceptosListView
from views.Gestion_haberes.conceptos.concepto_crear_editar_view import CrearEditarConceptoView
from views.Gestion_haberes.liquidacion.datos_fijos.datos_fijos_view import DatosFijosView
from views.Gestion_haberes.liquidacion.datos_fijos.crear_edicion_datos_fijos_view import DatosFijosAltaEdicionView
from views.Gestion_haberes.liquidacion.liquidacion__haberes.liquidacion_haberes_view import LiquidacionDeHaberesView 
from views.Gestion_haberes.liquidacion.liquidacion__haberes.crear_edicion_liquidacion_haberes_view import LiquidacionHaberesAltaEdicionView
from views.usuarios.usuarios_view import UsuariosView
from views.usuarios.usuario_crear_view import CrearUsuarioView
from views.usuarios.usuario_cambiar_password import CambiarPasswordView
from views.permiso_usuario.permiso_usuario_view import PermisoUsuarioView

class Layout:
    def __init__(self, page, on_logout):
        self.page = page
        self.on_logout = on_logout
              
        # =========================
        # SIDEBAR
        # =========================
        self.sidebar = Sidebar(
            page,
            on_logout,
            self.change_view
        )

        # =========================
        # VIEWS
        # =========================

        self.views = {
            "dashboard" : DashboardView(page),
            "legajos": LegajosView(page),
            "crear_legajo": CrearLegajoView(page),
            "gestion_legajo": GestionLegajoLayout(page),
            "conceptos": ConceptosListView(page),
            "crear_concepto" : CrearEditarConceptoView(page),
            "novedades" : NovedadesView(page),
            "gestionar_usuarios" : UsuariosView(page),
            "crear_usuario": CrearUsuarioView(page),
            "cambiar_contrasena":CambiarPasswordView(page,   self.on_logout),
            "permiso_usuario": PermisoUsuarioView(page),
            "datos_fijos_liquidacion": DatosFijosView(page, self),
            "crear_editar_datos_fijos": DatosFijosAltaEdicionView(page, self),
            "liquidacion_haberes" :LiquidacionDeHaberesView(page),
            "crear_editar_liquidacion_haberes" :LiquidacionHaberesAltaEdicionView(page)
        }

        # =========================
        # CONTENT
        # =========================

        self.content = ft.Container(

            expand=True,

            padding=-8,
                 
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

    def change_view(self, view_name, *args):

     
        if view_name not in self.views:
            self.content.content = ft.Container(
                content=ft.Text(
                    f"Vista '{view_name}' en construcción",
                    size=26
                )
            )
            self.page.update()
            return None

        vista = self.views[view_name]

        # Configurar la vista
        if hasattr(vista, "set_mode") and args:
            vista.set_mode(*args)

        self.content.content = vista

        # Cargar datos si la vista lo necesita
        if hasattr(vista, "load"):
            self.page.run_task(vista.load, *args)

        self.page.update()

        return vista