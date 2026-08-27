import flet as ft
from decimal import Decimal
from datetime import datetime


class LiquidacionDetalleModal:

    def __init__(self, page):

        self.page = page

        # =====================================================
        # CONTROLES
        # =====================================================

        self.lbl_fecha = ft.Text(
            "-",
            size=12
        )

        self.lbl_periodo = ft.Text(
            "-",
            size=12
        )

        self.lbl_modalidad = ft.Text(
            "-",
            size=12
        )

        self.lbl_numero = ft.Text(
            "-",
            size=12
        )

        self.lbl_legajo = ft.Text(
            "-",
            size=12
        )

        self.lbl_ayn = ft.Text(
            "-",
            size=12
        )

        # =====================================================
        # TOTALES
        # =====================================================

        self.lbl_total_haberes = ft.Text(
            "$ 0,00",
            size=14,
            weight=ft.FontWeight.BOLD
        )

        self.lbl_total_retenciones = ft.Text(
            "$ 0,00",
            size=14,
            weight=ft.FontWeight.BOLD
        )

        self.lbl_total_neto = ft.Text(
            "$ 0,00",
            size=17,
            weight=ft.FontWeight.BOLD,
            color="green"
        )

        # =====================================================
        # LISTA DE CONCEPTOS
        # =====================================================

        self.lista_conceptos = ft.ListView(
            expand=True,
            spacing=0,
            auto_scroll=False
        )

        # =====================================================
        # DIALOG
        # =====================================================

        self.dialog = ft.AlertDialog(

            modal=True,

            title=ft.Text(
                "Liquidación de haberes",
                size=18,
                weight=ft.FontWeight.BOLD
            ),

            content=ft.Container(
                width=1000,
                height=600,
                content=self.contenido()
            ),

            actions=[
                ft.OutlinedButton(
                    "Cerrar",
                    icon=ft.Icons.CLOSE,
                    on_click=self.cerrar
                )
            ],

            actions_alignment=ft.MainAxisAlignment.END
        )

    # =========================================================
    # CONTENIDO
    # =========================================================

    def contenido(self):

        return ft.Column(

            expand=True,

            spacing=10,

            controls=[

                self.cabecera(),

                self.detalle(),

                self.totales()

            ]
        )

    # =========================================================
    # CABECERA
    # =========================================================

    def cabecera(self):

        return ft.Container(

            bgcolor="white",

            padding=12,

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            content=ft.Column(

                spacing=8,

                controls=[

                    ft.Text(
                        "Datos de la liquidación",
                        size=13,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Row(
                        spacing=30,

                        controls=[

                            self.campo(
                                "Fecha",
                                self.lbl_fecha
                            ),

                            self.campo(
                                "Período",
                                self.lbl_periodo
                            ),

                            self.campo(
                                "Modalidad",
                                self.lbl_modalidad
                            ),

                            self.campo(
                                "Número",
                                self.lbl_numero
                            )

                        ]
                    ),

                    ft.Row(

                        spacing=30,

                        controls=[

                            self.campo(
                                "Legajo",
                                self.lbl_legajo
                            ),

                            ft.Container(
                                expand=True,

                                content=self.campo(
                                    "Apellido y Nombre",
                                    self.lbl_ayn
                                )
                            )

                        ]
                    )

                ]
            )
        )

    # =========================================================
    # CAMPO
    # =========================================================

    def campo(self, titulo, control):

        return ft.Row(

            spacing=6,

            controls=[

                ft.Text(
                    f"{titulo}:",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                    color="#475569"
                ),

                control

            ]
        )

    # =========================================================
    # DETALLE
    # =========================================================

    def detalle(self):

        return ft.Container(

            expand=True,

            bgcolor="white",

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            content=ft.Column(

                expand=True,

                spacing=0,

                controls=[

                    ft.Container(

                        padding=10,

                        content=ft.Text(
                            "Conceptos liquidados",
                            size=14,
                            weight=ft.FontWeight.BOLD
                        )
                    ),

                    self.encabezado_grilla(),

                    ft.Container(
                        expand=True,
                        content=self.lista_conceptos
                    )

                ]
            )
        )

    # =========================================================
    # ENCABEZADO GRILLA
    # =========================================================

    def encabezado_grilla(self):

        return ft.Container(

            bgcolor="#E2E8F0",

            padding=8,

            content=ft.Row(

                spacing=8,

                controls=[

                    ft.Container(
                        width=80,

                        content=ft.Text(
                            "Código",
                            size=11,
                            weight=ft.FontWeight.BOLD
                        )
                    ),

                    ft.Container(
                        expand=3,

                        content=ft.Text(
                            "Concepto",
                            size=11,
                            weight=ft.FontWeight.BOLD
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            "Cantidad",
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.RIGHT
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            "Valor",
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.RIGHT
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            "Haberes",
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.RIGHT
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            "Retención",
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.RIGHT
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            "Total",
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.RIGHT
                        )
                    )

                ]
            )
        )

    # =========================================================
    # FILA
    # =========================================================

    def agregar_fila(self, item):

        cantidad = self.decimal(
            item.get("cantidad")
        )

        valor = self.decimal(
            item.get("valor")
        )

        haber = self.decimal(
            item.get("haber")
        )

        retencion = self.decimal(
            item.get("retencion")
        )

        total = self.decimal(
            item.get("total")
        )

        fila = ft.Container(

            padding=8,

            border=ft.Border(
                bottom=ft.BorderSide(
                    1,
                    "#E2E8F0"
                )
            ),

            content=ft.Row(

                spacing=8,

                controls=[

                    ft.Container(
                        width=80,

                        content=ft.Text(
                            str(
                                item.get(
                                    "codigo",
                                    ""
                                )
                            ),
                            size=11
                        )
                    ),

                    ft.Container(
                        expand=3,

                        content=ft.Text(
                            str(
                                item.get(
                                    "concepto",
                                    ""
                                )
                            ),
                            size=11
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            f"{cantidad:,.2f}",
                            size=11,
                            text_align=ft.TextAlign.RIGHT
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            f"{valor:,.2f}",
                            size=11,
                            text_align=ft.TextAlign.RIGHT
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            f"{haber:,.2f}",
                            size=11,
                            text_align=ft.TextAlign.RIGHT
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            f"{retencion:,.2f}",
                            size=11,
                            text_align=ft.TextAlign.RIGHT
                        )
                    ),

                    ft.Container(
                        expand=1,

                        content=ft.Text(
                            f"{total:,.2f}",
                            size=11,
                            text_align=ft.TextAlign.RIGHT
                        )
                    )

                ]
            )
        )

        self.lista_conceptos.controls.append(
            fila
        )

    # =========================================================
    # TOTALES
    # =========================================================

    def totales(self):

        return ft.Container(

            bgcolor="white",

            padding=10,

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            content=ft.Row(

                alignment=ft.MainAxisAlignment.END,

                controls=[

                    ft.Column(

                        spacing=5,

                        controls=[

                            ft.Row(

                                width=350,

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Total Haberes:",
                                        weight=ft.FontWeight.BOLD
                                    ),

                                    self.lbl_total_haberes

                                ]
                            ),

                            ft.Row(

                                width=350,

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Total Retenciones:",
                                        weight=ft.FontWeight.BOLD
                                    ),

                                    self.lbl_total_retenciones

                                ]
                            ),

                            ft.Divider(
                                height=5
                            ),

                            ft.Row(

                                width=350,

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Neto a Cobrar:",
                                        size=15,
                                        weight=ft.FontWeight.BOLD
                                    ),

                                    self.lbl_total_neto

                                ]
                            )

                        ]
                    )
                ]
            )
        )

    # =========================================================
    # MOSTRAR
    # =========================================================
    def mostrar(self, data):

        if not data:
            return

        # -----------------------------------------------------
        # Limpiar detalle anterior
        # -----------------------------------------------------

        self.lista_conceptos.controls.clear()

        # -----------------------------------------------------
        # Cabecera
        # -----------------------------------------------------

        self.lbl_fecha.value = self.formatear_fecha(
            data.get("fecha")
        )

        self.lbl_periodo.value = str(
            data.get("periodo", "")
        )

        self.lbl_modalidad.value = str(
            data.get("modalidad", "")
        )

        self.lbl_numero.value = str(
            data.get("numero", "")
        )

        self.lbl_legajo.value = str(
            data.get("legajo_id", "")
        )

        self.lbl_ayn.value = str(
            data.get("ayn", "")
        )

        # -----------------------------------------------------
        # Totales
        # -----------------------------------------------------

        self.lbl_total_haberes.value = self.moneda(
            data.get("total_haberes")
        )

        self.lbl_total_retenciones.value = self.moneda(
            data.get("total_retenciones")
        )

        self.lbl_total_neto.value = self.moneda(
            data.get("total_neto")
        )

        # -----------------------------------------------------
        # Detalle
        # -----------------------------------------------------

        for item in data.get("lineas", []):

            self.agregar_fila(item)

        # -----------------------------------------------------
        # AGREGAR EL DIALOG AL OVERLAY
        # -----------------------------------------------------

        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)

        # -----------------------------------------------------
        # Abrir
        # -----------------------------------------------------

        self.dialog.open = True

        self.page.update()
    # =========================================================
    # CERRAR
    # =========================================================

    def cerrar(self, e):

        self.dialog.open = False

        self.page.update()

    # =========================================================
    # DECIMAL
    # =========================================================

    def decimal(self, valor):

        if valor is None:
            return Decimal("0")

        try:

            return Decimal(
                str(valor)
            )

        except Exception:

            return Decimal("0")

    # =========================================================
    # FECHA
    # =========================================================

    def formatear_fecha(self, fecha):

        if fecha is None:
            return "-"

        try:

            if isinstance(
                fecha,
                datetime
            ):

                dt = fecha

            else:

                fecha = str(
                    fecha
                )

                dt = datetime.fromisoformat(
                    fecha
                )

            return dt.strftime(
                "%d/%m/%Y %H:%M"
            )

        except Exception:

            return str(
                fecha
            )

    # =========================================================
    # MONEDA
    # =========================================================

    def moneda(self, valor):

        if valor is None:
            return "$ 0,00"

        try:

            valor = Decimal(
                str(valor)
            )

            return f"$ {valor:,.2f}"

        except Exception:

            return "$ 0,00"