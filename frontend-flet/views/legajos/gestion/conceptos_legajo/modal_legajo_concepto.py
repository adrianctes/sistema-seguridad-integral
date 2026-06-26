import flet as ft
import httpx

from core.config import settings
from components.alerts import Toast


class ModalLegajoConcepto(ft.AlertDialog):

    def __init__(self, page, callback):

        super().__init__()

        self.page_ref = page
        self.callback = callback

        self.legajo_id = 0
        self.item_id = 0

        self.toast = Toast()

        self.modal = True

        self.txt_valor = ft.TextField(
            label="Valor",
            border_radius=0
        )

        self.chk_activo = ft.Checkbox(
            label="Activo",
            value=True
        )

        self.dp_desde = ft.TextField(
            label="Desde",
            border_radius=0
        )

        self.dp_hasta = ft.TextField(
            label="Hasta",
            border_radius=0
        )

        self.cmb_concepto = ft.Dropdown(

            label="Concepto",

            border_radius=0,

            options=[]
        )

        self.content = ft.Container(

            width=600,

            content=ft.Column(

                tight=True,

                controls=[

                    self.cmb_concepto,

                    ft.Row([

                        self.dp_desde,

                        self.dp_hasta

                    ]),

                    self.txt_valor,

                    self.chk_activo
                ]
            )
        )

        self.actions = [

            ft.TextButton(
                "Cancelar",
                on_click=self.cerrar
            ),

            ft.FilledButton(
                "Guardar",
                on_click=self.guardar
            )
        ]

    async def abrir(self, legajo_id, item=None):

        self.legajo_id = legajo_id

        await self.cargar_conceptos()

        self.limpiar()

        if item:

            self.item_id = item["id"]

            self.cmb_concepto.value = str(
                item["concepto_id"]
            )

            self.dp_desde.value = (
                item["fecha_desde"]
            )

            self.dp_hasta.value = (
                item["fecha_hasta"] or ""
            )

            self.txt_valor.value = (
                str(
                    item["valor"]
                )
            )

            self.chk_activo.value = (
                item["activo"]
            )

        self.open = True

        self.page_ref.dialog = self

        self.page_ref.update()

    async def cargar_conceptos(self):

        async with httpx.AsyncClient() as client:

            r = await client.get(

                f"{settings.URL_BACKEND}/conceptos",

                headers={
                    "Authorization":
                    f"Bearer {settings.TOKEN}"
                }
            )

        data = r.json()

        self.cmb_concepto.options = [

            ft.dropdown.Option(

                str(x["id"]),

                x["nombre"]

            )

            for x in data
        ]

    def limpiar(self):

        self.item_id = 0

        self.cmb_concepto.value = None

        self.dp_desde.value = ""

        self.dp_hasta.value = ""

        self.txt_valor.value = ""

        self.chk_activo.value = True

    async def guardar(self, e):

        data = {

            "legajo_id":
            self.legajo_id,

            "concepto_id":
            int(
                self.cmb_concepto.value
            ),

            "fecha_desde":
            self.dp_desde.value,

            "fecha_hasta":
            self.dp_hasta.value,

            "valor":
            float(
                self.txt_valor.value
                or 0
            ),

            "activo":
            self.chk_activo.value
        }

        async with httpx.AsyncClient() as client:

            if self.item_id:

                await client.put(

                    f"{settings.URL_BACKEND}/legajo-conceptos/{self.item_id}",

                    json=data,

                    headers={
                        "Authorization":
                        f"Bearer {settings.TOKEN}"
                    }
                )

            else:

                await client.post(

                    f"{settings.URL_BACKEND}/legajo-conceptos",

                    json=data,

                    headers={
                        "Authorization":
                        f"Bearer {settings.TOKEN}"
                    }
                )

        self.open = False

        await self.callback()

        self.page_ref.update()

    def cerrar(self, e):

        self.open = False

        self.page_ref.update()