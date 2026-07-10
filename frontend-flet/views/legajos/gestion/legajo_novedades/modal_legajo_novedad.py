import asyncio

import flet as ft
import httpx

from core.config import settings
from components.alerts import Toast
from components.datapicker import DatePickerCustom


class ModalLegajoNovedad(ft.AlertDialog):

    def __init__(self, page, on_success=None):

        super().__init__(modal=True)

        self.page_ref = page
        self.on_success = on_success

        self.legajo_id = 0
        self.item_id = 0
        self.modalidad_pago_id = 0

        self.toast = Toast()

        self.shape = ft.RoundedRectangleBorder(radius=0)

        self.bgcolor = "white"

        self.content_padding = 0

        self.inset_padding = 20

        # =========================
        # TITLE
        # =========================

        self.titulo_accion = "Agregar Nueva Novedad"

        self.lbl_titulo_accion = ft.Text(
            self.titulo_accion,
            size=18,
            weight=ft.FontWeight.BOLD
        )

        self.lbl_mensaje = ft.Text(
            "",
            size=14,
            color=ft.Colors.RED_400,
            visible=False,
            margin=ft.Margin(0, 10, 0, 12),
        )

        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[

                ft.Column(
                    spacing=2,
                    tight=True,
                    controls=[
                        self.lbl_titulo_accion,
                        self.lbl_mensaje
                    ]
                ),

                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=18,
                    tooltip="Cerrar",
                    padding=0,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=0
                        )
                    ),
                    on_click=self.cerrar
                )
            ]
        )

        # =========================
        # CONTROLES
        # =========================

        self.cmb_concepto = ft.Dropdown(
            label="Concepto",
            options=[],
            expand=True
        )

        self.dp_desde = DatePickerCustom(
            self.page_ref,
            label="Fecha Desde"
        )

        self.dp_hasta = DatePickerCustom(
            self.page_ref,
            label="Fecha Hasta"
        )

        self.txt_periodo = ft.TextField(
            label="Período",
            hint_text="202607",
            max_length=6,
            expand=True
        )

        self.txt_cantidad = ft.TextField(
            label="Cantidad",
            value="1.00",
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            on_change=self.solo_decimal
        )

        self.txt_valor = ft.TextField(
            label="Valor",
            value="0.00",
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
            on_change=self.valor_formateado_decimal
        )

        self.chk_activo = ft.Checkbox(
            label="Activo",
            value=True
        )

        self.loading = ft.ProgressRing(
            visible=False
        )

        # =========================
        # CONTENT
        # =========================

        self.content = ft.Container(

            width=700,

            padding=15,

            content=ft.Column(

                spacing=10,

                tight=True,

                controls=[

                    ft.Container(
                        margin=ft.Margin(0, -14, 0, 0),
                        content=self.cmb_concepto
                    ),

                    ft.Row(
                        spacing=10,
                        controls=[

                            ft.Container(
                                expand=1,
                                content=self.dp_desde
                            ),

                            ft.Container(
                                expand=1,
                                content=self.dp_hasta
                            ),
                        ]
                    ),

                    ft.Row(
                        spacing=10,
                        controls=[

                            ft.Container(
                                expand=1,
                                content=self.txt_periodo
                            ),

                            ft.Container(
                                expand=1,
                                content=self.txt_cantidad
                            ),

                            ft.Container(
                                expand=1,
                                content=self.txt_valor
                            ),
                        ]
                    ),

                    ft.Container(
                        margin=ft.Margin(0, 4, 0, 0),
                        content=self.chk_activo
                    ),

                    ft.Container(
                        margin=ft.Margin(0, 4, 0, 0),
                        content=self.lbl_mensaje
                    ),

                    ft.Divider(height=1),

                    ft.Row(

                        alignment=ft.MainAxisAlignment.END,

                        vertical_alignment=ft.CrossAxisAlignment.CENTER,

                        controls=[

                            self.loading,

                            ft.OutlinedButton(
                                "Cancelar",
                                style=ft.ButtonStyle(
                                    padding=12
                                ),
                                on_click=self.cerrar
                            ),

                            ft.FilledButton(
                                "Guardar",
                                icon=ft.Icons.SAVE,
                                style=ft.ButtonStyle(
                                    bgcolor="#0F172A",
                                    color="white",
                                    padding=12
                                ),
                                on_click=self.guardar
                            )
                        ]
                    )
                ]
            )
        )
        # =====================================================
    # ABRIR
    # =====================================================

    async def abrir(self, legajo_id, item=None):

        self.limpiar()

        self.legajo_id = legajo_id

        legajo = await self.obtener_legajo_by_id(legajo_id)

        if legajo:
            self.modalidad_pago_id = legajo.get("modalidad_pago_id")

        await self.cargar_conceptos()

        self.cmb_concepto.disabled = False

        self.item_id = 0

        self.lbl_titulo_accion.value = "Agregar Nueva Novedad"

        if item:

            self.lbl_titulo_accion.value = "Editar Novedad"

            self.item_id = item["id"]

            self.cmb_concepto.value = str(item["concepto_id"])

            self.cmb_concepto.disabled = True

            self.dp_desde.value = item["fecha_desde"]

            self.dp_hasta.value = item["fecha_hasta"] or ""

            self.txt_periodo.value = item["periodo"]

            self.txt_cantidad.value = str(item["cantidad"])

            self.txt_valor.value = (
                f"{float(item['valor']):,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            self.chk_activo.value = item.get(
                "activo",
                True
            )

        if self not in self.page_ref.overlay:
            self.page_ref.overlay.append(self)

        self.page_ref.dialog = self

        self.open = True

        self.page_ref.update()


    # =====================================================
    # CARGAR CONCEPTOS
    # =====================================================

    async def cargar_conceptos(self):

        async with httpx.AsyncClient() as client:

            response = await client.get(

                f"{settings.URL_BACKEND}/conceptos/modalidad-pago/{self.modalidad_pago_id}",

                headers={
                    "Authorization": f"Bearer {settings.TOKEN}"
                }
            )

        if response.status_code != 200:
            return

        self.cmb_concepto.options = [

            ft.dropdown.Option(
                str(x["id"]),
                x["nombre"]
            )

            for x in response.json()
        ]


    # =====================================================
    # LIMPIAR
    # =====================================================

    def limpiar(self):

        self.item_id = 0

        self.cmb_concepto.value = None

        self.cmb_concepto.error_text = None

        self.cmb_concepto.disabled = False

        self.dp_desde.value = ""

        self.dp_hasta.value = ""

        self.txt_periodo.value = ""

        self.txt_cantidad.value = "1.00"

        self.txt_valor.value = "0.00"

        self.chk_activo.value = True

        self.lbl_mensaje.visible = False

        self.lbl_mensaje.value = ""

        self.lbl_titulo_accion.value = (
            "Agregar Nueva Novedad"
        )


    # =====================================================
    # OBTENER LEGAJO
    # =====================================================

    async def obtener_legajo_by_id(self, legajo_id: int):

        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/legajos/{legajo_id}"

        async with httpx.AsyncClient() as client:

            response = await client.get(

                url,

                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        if response.status_code != 200:

            await self.toast.show(
                self.page_ref,
                f"Error API: {response.status_code}",
                "error"
            )

            return None

        data = response.json()

        return {

            "id": data.get("id"),

            "modalidad_pago_id": data.get(
                "modalidad_pago_id"
            )
        }
    def cerrar(self, e=None):

        self.open = False

        self.page_ref.dialog = None

        self.page_ref.update()
    async def guardar(self, e):
        pass

    async def validar_formulario(self):
        return True

    async def api_crear(self, data):
        return True

    async def api_editar(self, data):
        return True

    def solo_decimal(self, e):
        pass

    def valor_formateado_decimal(self, e):
        pass