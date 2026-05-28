import flet as ft


class LicenciasView(ft.Container):

    def __init__(self, page):
        super().__init__()

        self.page_ref = page

        self.expand = True

        self.padding = 20

        self.lbl = ft.Text("Cargando...")

        self.content = ft.Column(
            spacing=10,
            controls=[
                ft.Text("Licencias"),
                self.lbl,
            ]
        )

    async def load(self, legajo_id=None):

        self.lbl.value = "Pagina en Contruccion"

        self.page_ref.update()