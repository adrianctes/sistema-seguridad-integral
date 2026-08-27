""" '''import flet as ft
import calendar
import datetime


class DatePickerCustom(ft.Container):

    def __init__(self, page, label="Fecha", on_change=None):

        super().__init__()

        self.page_ref = page

        self.on_change = on_change

        self.selected_date = None

        self.current_date = datetime.date.today()

        # =====================================
        # INPUT
        # =====================================

        self.input = ft.TextField(
            label=label,
            read_only=True,
            height=55,
            expand=True,
            filled=True,
            border_radius=0,
            border_color="#CBD5E1",
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.open_calendar,
        )

        self.content = self.input

        self.dialog = None

    def open_calendar(self, e):

        if not self.dialog:

            self.dialog = ft.AlertDialog(
                shape=ft.RoundedRectangleBorder(radius=0),
                content=self.build_calendar(),
            )

            self.page_ref.overlay.append(
                self.dialog
            )

        self.dialog.open = True

        self.page_ref.update()

    def build_calendar(self):

        year = self.current_date.year

        month = self.current_date.month

        cal = calendar.monthcalendar(
            year,
            month
        )


        header = ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            controls=[

                ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=self.prev_month,
                ),

                ft.Text(
                    f"{calendar.month_name[month]} {year}",
                    size=16
                ),

                ft.IconButton(
                    ft.Icons.CHEVRON_RIGHT,
                    on_click=self.next_month,
                ),
            ],
        )

        # =====================================
        # WEEK DAYS
        # =====================================

        week_days = ft.Row(

            controls=[

                ft.Text(
                    d,
                    width=30,
                    text_align="center"
                )

                for d in [
                    "L",
                    "M",
                    "X",
                    "J",
                    "V",
                    "S",
                    "D"
                ]
            ]
        )

      

        days_controls = []

        for week in cal:

            row = ft.Row()

            for day in week:

                if day == 0:

                    row.controls.append(
                        ft.Container(
                            width=30,
                            height=30
                        )
                    )

                else:

                    row.controls.append(

                        ft.Container(

                            width=30,

                            height=30,

                            alignment=ft.Alignment(0, 0),

                            bgcolor=(
                                "#F1F5F9"
                                if self.is_selected(day)
                                else None
                            ),

                            border=ft.Border(

                                left=ft.BorderSide(
                                    1,
                                    "#E2E8F0"
                                ),

                                top=ft.BorderSide(
                                    1,
                                    "#E2E8F0"
                                ),

                                right=ft.BorderSide(
                                    1,
                                    "#E2E8F0"
                                ),

                                bottom=ft.BorderSide(
                                    1,
                                    "#E2E8F0"
                                ),
                            ),

                            content=ft.Text(
                                str(day)
                            ),

                            on_click=lambda e, d=day:
                                self.select_day(d),
                        )
                    )

            days_controls.append(row)

        return ft.Container(

            width=320,

            padding=10,

            content=ft.Column(

                tight=True,

                controls=[
                    header,
                    week_days,
                    ft.Column(days_controls),
                ],
            ),
        )

    def select_day(self, day):

        self.selected_date = datetime.date(

            self.current_date.year,

            self.current_date.month,

            day,
        )

        self.input.value = (
            self.selected_date.strftime(
                "%d/%m/%Y"
            )
        )

        if self.on_change:

            self.on_change(
                self.selected_date
            )

        self.close()

    def next_month(self, e):

        self.current_date = self.add_months(
            self.current_date,
            1
        )

        self.refresh()

    def prev_month(self, e):

        self.current_date = self.add_months(
            self.current_date,
            -1
        )

        self.refresh()

    def refresh(self):

        self.dialog.content = (
            self.build_calendar()
        )

        self.page_ref.update()

    def add_months(self, source_date, months):

        month = source_date.month - 1 + months

        year = source_date.year + month // 12

        month = month % 12 + 1

        return datetime.date(
            year,
            month,
            1
        )

    def is_selected(self, day):

        if not self.selected_date:
            return False

        return (

            self.selected_date.year ==
            self.current_date.year

            and

            self.selected_date.month ==
            self.current_date.month

            and

            self.selected_date.day == day
        )

    def close(self):

        if self.dialog:

            self.dialog.open = False

            self.page_ref.update()

    def reset(self):

        self.input.value = ""

        self.selected_date = None

        self.current_date = datetime.date.today()

        self.input.error= None

        self.page_ref.update()

    def set_error(self, message):
        self.input.error = message
        self.page_ref.update()

    def clear_error(self):
        self.input.error = None
        self.page_ref.update()
    
    def get_value(self):

        if not self.selected_date:
            return None

        return self.selected_date.strftime("%Y-%m-%d")
    
    def set_value(self, value):

        if value is None:
            self.selected_date = None
            self.input.value = ""
            self.current_date = datetime.date.today()

        else:
            if isinstance(value, str):
                value = datetime.datetime.strptime(value, "%Y-%m-%d").date()

            elif isinstance(value, datetime.datetime):
                value = value.date()

            self.selected_date = value
            self.current_date = value
            self.input.value = value.strftime("%d/%m/%Y")

        self.page_ref.update()
    '''
import flet as ft
import calendar
import datetime


class DatePickerCustom(ft.Container):

    def __init__(
        self,
        page,
        label="Fecha",
        on_change=None,
        modo="fecha"      # fecha | periodo
    ):

        super().__init__()

        self.page_ref = page
        self.on_change = on_change
        self.modo = modo

        self.selected_date = None
        self.current_date = datetime.date.today()

        self.input = ft.TextField(
            label=label,
            read_only=True,
            height=55,
            expand=True,
            filled=True,
            border_radius=0,
            border_color="#CBD5E1",
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.open_calendar,
        )

        self.content = self.input

        self.dialog = None

    # -----------------------------------------------------
    # ABRIR DIALOGO
    # -----------------------------------------------------

    def open_calendar(self, e):

        if not self.dialog:

            self.dialog = ft.AlertDialog(
                shape=ft.RoundedRectangleBorder(radius=0),
                content=self.build_calendar(),
            )

            self.page_ref.overlay.append(
                self.dialog
            )

        self.dialog.open = True
        self.page_ref.update()

    # -----------------------------------------------------
    # CONSTRUIR CALENDARIO
    # -----------------------------------------------------

    def build_calendar(self):

        if self.modo == "periodo":
            return self.build_period_picker()

        year = self.current_date.year
        month = self.current_date.month

        cal = calendar.monthcalendar(
            year,
            month
        )

        header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=self.prev_month,
                ),
                ft.Text(
                    f"{calendar.month_name[month]} {year}",
                    size=16,
                ),
                ft.IconButton(
                    ft.Icons.CHEVRON_RIGHT,
                    on_click=self.next_month,
                ),
            ],
        )

        week_days = ft.Row(
            controls=[
                ft.Text(
                    d,
                    width=30,
                    text_align="center",
                )
                for d in [
                    "L",
                    "M",
                    "X",
                    "J",
                    "V",
                    "S",
                    "D",
                ]
            ]
        )

        days_controls = []

        for week in cal:

            row = ft.Row()

            for day in week:

                if day == 0:

                    row.controls.append(
                        ft.Container(
                            width=30,
                            height=30,
                        )
                    )

                else:

                    row.controls.append(

                        ft.Container(

                            width=30,
                            height=30,

                            alignment=ft.Alignment(0, 0),

                            bgcolor=(
                                "#077CF1"
                                if self.is_selected(day)
                                else None
                            ),
                            border_radius=20,

                            border=ft.Border(
                                left=ft.BorderSide(1, "#E2E8F0"),
                                top=ft.BorderSide(1, "#E2E8F0"),
                                right=ft.BorderSide(1, "#E2E8F0"),
                                bottom=ft.BorderSide(1, "#E2E8F0"),
                            ),

                            content=ft.Text(str(day)),

                            on_click=lambda e, d=day:
                                self.select_day(d),
                        )
                    )

            days_controls.append(row)

        return ft.Container(
            width=320,
            padding=10,
            content=ft.Column(
                tight=True,
                controls=[
                    header,
                    week_days,
                    ft.Column(days_controls),
                ],
            ),
        )

    # -----------------------------------------------------
    # SELECTOR DE PERIODO
    # -----------------------------------------------------

    def build_period_picker(self):

        meses = [
            "Ene", "Feb", "Mar", "Abr",
            "May", "Jun", "Jul", "Ago",
            "Sep", "Oct", "Nov", "Dic"
        ]

        header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    on_click=self.prev_year,
                ),
                ft.Text(
                    str(self.current_date.year),
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.IconButton(
                    ft.Icons.CHEVRON_RIGHT,
                    on_click=self.next_year,
                ),
            ],
        )

        rows = []

        indice = 0

        for _ in range(3):

            controls = []

            for _ in range(4):

                numero_mes = indice + 1

                seleccionado = (
                    self.selected_date is not None
                    and self.selected_date.year == self.current_date.year
                    and self.selected_date.month == numero_mes
                )

                controls.append(

                    ft.Container(

                        width=65,
                        height=45,

                        alignment=ft.Alignment.CENTER,

                        bgcolor=(
                            "#2563EB"
                            if seleccionado
                            else "#F8FAFC"
                        ),

                        border=ft.Border(
                            left=ft.BorderSide(1, "#CBD5E1"),
                            top=ft.BorderSide(1, "#CBD5E1"),
                            right=ft.BorderSide(1, "#CBD5E1"),
                            bottom=ft.BorderSide(1, "#CBD5E1"),
                        ),

                        border_radius=4,

                        content=ft.Text(

                            meses[indice],

                            color=(
                                "white"
                                if seleccionado
                                else "black"
                            ),

                            weight=(
                                ft.FontWeight.BOLD
                                if seleccionado
                                else ft.FontWeight.NORMAL
                            ),
                        ),

                        on_click=lambda e, m=numero_mes:
                            self.select_month(m),
                    )
                )

                indice += 1

            rows.append(ft.Row(
                controls,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            ))

        return ft.Container(

            width=320,

            padding=10,

            content=ft.Column(

                tight=True,

                controls=[
                    header,
                    ft.Divider(height=10),
                    *rows
                ],
            ),
        )

    # ---------------------------------------------------------
    # NAVEGACION ENTRE AÑOS
    # ---------------------------------------------------------

    def next_year(self, e):

        self.current_date = datetime.date(
            self.current_date.year + 1,
            self.current_date.month,
            1
        )

        self.refresh()

    def prev_year(self, e):

        self.current_date = datetime.date(
            self.current_date.year - 1,
            self.current_date.month,
            1
        )

        self.refresh()

    # ---------------------------------------------------------
    # SELECCION DEL MES
    # ---------------------------------------------------------

    def select_month(self, month):

        self.selected_date = datetime.date(

            self.current_date.year,

            month,

            1
        )

        self.current_date = self.selected_date

        self.input.value = self.selected_date.strftime("%m/%Y")

        if self.on_change:

            self.on_change(self.selected_date)

        self.close()
    
    def select_day(self, day):

        self.selected_date = datetime.date(
            self.current_date.year,
            self.current_date.month,
            day,
        )

        if self.modo == "periodo":
            self.selected_date = self.selected_date.replace(day=1)
            self.input.value = self.selected_date.strftime("%m/%Y")
        else:
            self.input.value = self.selected_date.strftime("%d/%m/%Y")

        if self.on_change:
            self.on_change(self.selected_date)

        self.close()
    
    def set_value(self, value):

        if value is None:
            self.selected_date = None
            self.input.value = ""
            self.current_date = datetime.date.today()

        else:
            if isinstance(value, str):
                value = datetime.datetime.strptime(value, "%Y-%m-%d").date()

            elif isinstance(value, datetime.datetime):
                value = value.date()

            self.selected_date = value
            self.current_date = value
            self.input.value = value.strftime("%d/%m/%Y")

            if self.page is not None:
                 self.update()
    
    def refresh(self):

        self.dialog.content = self.build_calendar()

        self.page_ref.update()

    def close(self):

        if self.dialog:

            self.dialog.open = False

            self.page_ref.update()

    def reset(self):

        self.input.value = ""

        self.selected_date = None

        self.current_date = datetime.date.today()

        self.input.error= None

        #if self.dialog:
        #    self.dialog.content = self.build_calendar()


        self.page_ref.update()

    def set_error(self, message):
        self.input.error = message
        self.page_ref.update()

    def clear_error(self):
        self.input.error = None
        self.page_ref.update()
    
    def get_value(self):

        if not self.selected_date:
            return None

        return self.selected_date.strftime("%Y-%m-%d")
    
    def set_value(self, value):

        if value is None:
            self.selected_date = None
            self.input.value = ""
            self.current_date = datetime.date.today()

        else:
            if isinstance(value, str):
                value = datetime.datetime.strptime(value, "%Y-%m-%d").date()

            elif isinstance(value, datetime.datetime):
                value = value.date()

            self.selected_date = value
            self.current_date = value
            self.input.value = value.strftime("%d/%m/%Y")

        self.page_ref.update()
    
    def prev_month(self, e):

        self.current_date = self.add_months(
            self.current_date,
            -1
        )

        self.refresh()
    
    def next_month(self, e):

        self.current_date = self.add_months(
            self.current_date,
            1
        )

        self.refresh()
    
    def is_selected(self, day):

        if not self.selected_date:
            return False

        return (

            self.selected_date.year ==
            self.current_date.year

            and

            self.selected_date.month ==
            self.current_date.month

            and

            self.selected_date.day == day
        )
    def add_months(self, source_date, months):

        month = source_date.month - 1 + months

        year = source_date.year + month // 12

        month = month % 12 + 1

        return datetime.date(
            year,
            month,
            1
        )

 """
import flet as ft
import calendar
import datetime


class DatePickerCustom(ft.Container):

    def __init__(
        self,
        page,
        label="Fecha",
        on_change=None,
        modo="fecha",  # fecha | periodo
    ):

        super().__init__()

        self.page_ref = page
        self.on_change = on_change
        self.modo = modo

        # ==========================================
        # ESTADO
        # ==========================================

        self.selected_date = None

        # Mes/año que se está mostrando
        self.current_date = datetime.date.today()

        # ==========================================
        # INPUT
        # ==========================================

        self.input = ft.TextField(
            label=label,
            read_only=True,
            height=55,
            expand=True,
            filled=True,
            border_radius=0,
            border_color="#CBD5E1",
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            on_click=self.open_calendar,
        )

        self.content = self.input

        # Dialogo del calendario
        self.dialog = None

    # ==========================================================
    # ABRIR CALENDARIO
    # ==========================================================
    def open_calendar(self, e=None):

        # ======================================================
        # POSICIONAR EL CALENDARIO EN LA FECHA SELECCIONADA
        # ======================================================

        if self.selected_date:

            self.current_date = datetime.date(
                self.selected_date.year,
                self.selected_date.month,
                1,
            )

        # ======================================================
        # CONSTRUIR / ACTUALIZAR DIÁLOGO
        # ======================================================

        if not self.dialog:

            self.dialog = ft.AlertDialog(
                shape=ft.RoundedRectangleBorder(
                    radius=0
                ),
                content=self.build_calendar(),
            )

            self.page_ref.overlay.append(
                self.dialog
            )

        else:

            self.dialog.content = (
                self.build_calendar()
            )

        # ======================================================
        # MOSTRAR
        # ======================================================

        self.dialog.open = True

        self.page_ref.update()
        
        # ==========================================================
        # CONSTRUIR CALENDARIO
        # ==========================================================

    def build_calendar(self):

        if self.modo == "periodo":

            return self.build_period_picker()

        year = self.current_date.year
        month = self.current_date.month

        cal = calendar.monthcalendar(
            year,
            month
        )

        # ======================================================
        # HEADER
        # ======================================================

        header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            controls=[

                ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT,
                    on_click=self.prev_month,
                ),

                ft.Text(
                    f"{calendar.month_name[month]} {year}",
                    size=16,
                ),

                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    on_click=self.next_month,
                ),
            ],
        )

        # ======================================================
        # DÍAS DE LA SEMANA
        # ======================================================

        week_days = ft.Row(
            controls=[

                ft.Text(
                    d,
                    width=30,
                    text_align=ft.TextAlign.CENTER,
                )

                for d in [
                    "L",
                    "M",
                    "X",
                    "J",
                    "V",
                    "S",
                    "D",
                ]
            ]
        )

        # ======================================================
        # DÍAS DEL MES
        # ======================================================

        days_controls = []

        for week in cal:

            row = ft.Row(
                spacing=0
            )

            for day in week:

                # ------------------------------------------------
                # Espacio vacío
                # ------------------------------------------------

                if day == 0:

                    row.controls.append(
                        ft.Container(
                            width=40,
                            height=30,
                        )
                    )

                    continue

                # ------------------------------------------------
                # Determinar si es el día seleccionado
                # ------------------------------------------------

                seleccionado = self.is_selected(day)

                # ------------------------------------------------
                # Día
                # ------------------------------------------------

                day_container = ft.Container(

                    width=40,
                    height=30,

                    alignment=ft.Alignment.CENTER,

                    bgcolor=(
                        "#2563EB"
                        if seleccionado
                        else None
                    ),

                    border_radius=20,

                    content=ft.Text(

                        str(day),
                        size=18,
                        color=(
                            "white"
                            if seleccionado
                            else "black"
                        ),

                        weight=(
                            ft.FontWeight.BOLD
                            if seleccionado
                            else ft.FontWeight.NORMAL
                        ),

                        text_align=ft.TextAlign.CENTER,
                    ),

                    on_click=lambda e, d=day:
                        self.select_day(d),
                )

                row.controls.append(
                    day_container
                )

            days_controls.append(row)

        # ======================================================
        # CONTENEDOR
        # ======================================================

        return ft.Container(

            width=320,

            padding=10,

            content=ft.Column(

                tight=True,

                controls=[

                    header,

                    ft.Container(
                        height=10
                    ),

                    week_days,

                    ft.Container(
                        height=5
                    ),

                    ft.Column(
                        days_controls,
                        spacing=2,
                    ),
                ],
            ),
        )

    # ==========================================================
    # SELECTOR DE PERÍODO
    # ==========================================================

    def build_period_picker(self):

        meses = [
            "Ene",
            "Feb",
            "Mar",
            "Abr",
            "May",
            "Jun",
            "Jul",
            "Ago",
            "Sep",
            "Oct",
            "Nov",
            "Dic",
        ]

        # ======================================================
        # HEADER
        # ======================================================

        header = ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            controls=[

                ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT,
                    on_click=self.prev_year,
                ),

                ft.Text(
                    str(self.current_date.year),
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    on_click=self.next_year,
                ),
            ],
        )

        # ======================================================
        # MESES
        # ======================================================

        rows = []

        indice = 0

        for _ in range(3):

            controls = []

            for _ in range(4):

                numero_mes = indice + 1

                seleccionado = (

                    self.selected_date is not None

                    and

                    self.selected_date.year
                    == self.current_date.year

                    and

                    self.selected_date.month
                    == numero_mes
                )

                controls.append(

                    ft.Container(

                        width=65,
                        height=45,

                        alignment=ft.Alignment.CENTER,

                        bgcolor=(

                            "#2563EB"

                            if seleccionado

                            else "#F8FAFC"
                        ),

                        border=ft.Border(

                            left=ft.BorderSide(
                                1,
                                "#CBD5E1"
                            ),

                            top=ft.BorderSide(
                                1,
                                "#CBD5E1"
                            ),

                            right=ft.BorderSide(
                                1,
                                "#CBD5E1"
                            ),

                            bottom=ft.BorderSide(
                                1,
                                "#CBD5E1"
                            ),
                        ),

                        border_radius=4,

                        content=ft.Text(

                            meses[indice],

                            color=(

                                "white"

                                if seleccionado

                                else "black"
                            ),

                            weight=(

                                ft.FontWeight.BOLD

                                if seleccionado

                                else ft.FontWeight.NORMAL
                            ),
                        ),

                        on_click=lambda e, m=numero_mes:
                            self.select_month(m),
                    )
                )

                indice += 1

            rows.append(

                ft.Row(

                    controls,

                    alignment=(
                        ft.MainAxisAlignment.SPACE_EVENLY
                    ),
                )
            )

        return ft.Container(

            width=320,

            padding=10,

            content=ft.Column(

                tight=True,

                controls=[

                    header,

                    ft.Divider(
                        height=10
                    ),

                    *rows,
                ],
            ),
        )

    # ==========================================================
    # NAVEGACIÓN MESES
    # ==========================================================

    def next_month(self, e=None):

        self.current_date = self.add_months(
            self.current_date,
            1
        )

        self.refresh()

    def prev_month(self, e=None):

        self.current_date = self.add_months(
            self.current_date,
            -1
        )

        self.refresh()

    # ==========================================================
    # NAVEGACIÓN AÑOS
    # ==========================================================

    def next_year(self, e=None):

        self.current_date = datetime.date(
            self.current_date.year + 1,
            self.current_date.month,
            1,
        )

        self.refresh()

    def prev_year(self, e=None):

        self.current_date = datetime.date(
            self.current_date.year - 1,
            self.current_date.month,
            1,
        )

        self.refresh()

    # ==========================================================
    # SELECCIONAR MES
    # ==========================================================

    def select_month(self, month):

        self.selected_date = datetime.date(
            self.current_date.year,
            month,
            1,
        )

        self.current_date = self.selected_date

        self.input.value = (
            self.selected_date.strftime(
                "%m/%Y"
            )
        )

        if self.on_change:

            self.on_change(
                self.selected_date
            )

        self.close()

    # ==========================================================
    # SELECCIONAR DÍA
    # ==========================================================

    def select_day(self, day):

        self.selected_date = datetime.date(

            self.current_date.year,

            self.current_date.month,

            day,
        )

        # ======================================================
        # MODO PERÍODO
        # ======================================================

        if self.modo == "periodo":

            self.selected_date = (
                self.selected_date.replace(
                    day=1
                )
            )

            self.input.value = (
                self.selected_date.strftime(
                    "%m/%Y"
                )
            )

        # ======================================================
        # MODO FECHA
        # ======================================================

        else:

            self.input.value = (
                self.selected_date.strftime(
                    "%d/%m/%Y"
                )
            )

        # ======================================================
        # CALLBACK
        # ======================================================

        if self.on_change:

            self.on_change(
                self.selected_date
            )

        self.close()

    # ==========================================================
    # REFRESCAR CALENDARIO
    # ==========================================================

    def refresh(self):

        if not self.dialog:
            return

        self.dialog.content = (
            self.build_calendar()
        )

        self.page_ref.update()

    # ==========================================================
    # CERRAR
    # ==========================================================

    def close(self):

        if self.dialog:

            self.dialog.open = False

            self.page_ref.update()

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        self.input.value = ""

        self.selected_date = None

        # Volvemos al mes actual
        self.current_date = (
            datetime.date.today()
        )

        self.input.error = None

        # Si el diálogo ya existe,
        # reconstruimos el calendario.
        if self.dialog:

            self.dialog.content = (
                self.build_calendar()
            )

        self.page_ref.update()

    # ==========================================================
    # SET VALUE
    # ==========================================================

    def set_value(self, value):

        if value is None:

            self.selected_date = None

            self.input.value = ""

            self.current_date = (
                datetime.date.today()
            )

        else:

            # ----------------------------------------------
            # String
            # ----------------------------------------------

            if isinstance(value, str):

                value = (
                    datetime.datetime
                    .strptime(
                        value,
                        "%Y-%m-%d"
                    )
                    .date()
                )

            # ----------------------------------------------
            # datetime
            # ----------------------------------------------

            elif isinstance(
                value,
                datetime.datetime
            ):

                value = value.date()

            # ----------------------------------------------
            # date
            # ----------------------------------------------

            self.selected_date = value

            # Mostramos el mes de la fecha
            self.current_date = datetime.date(
                value.year,
                value.month,
                1,
            )

            # ----------------------------------------------
            # Texto
            # ----------------------------------------------

            if self.modo == "periodo":

                self.input.value = (
                    value.strftime(
                        "%m/%Y"
                    )
                )

            else:

                self.input.value = (
                    value.strftime(
                        "%d/%m/%Y"
                    )
                )

        # Reconstruimos el calendario
        if self.dialog:

            self.dialog.content = (
                self.build_calendar()
            )

        self.page_ref.update()

    # ==========================================================
    # GET VALUE
    # ==========================================================

    def get_value(self):

        if not self.selected_date:

            return None

        return self.selected_date.strftime(
            "%Y-%m-%d"
        )

    # ==========================================================
    # ERROR
    # ==========================================================

    def set_error(self, message):

        self.input.error_text = message

        self.page_ref.update()

    def clear_error(self):

        self.input.error_text = None

        self.page_ref.update()

    # ==========================================================
    # SABER SI UN DÍA ESTÁ SELECCIONADO
    # ==========================================================

    def is_selected(self, day):

            # Fecha realmente seleccionada
            if self.selected_date:

                return (
                    self.selected_date.year
                    == self.current_date.year
                    and
                    self.selected_date.month
                    == self.current_date.month
                    and
                    self.selected_date.day
                    == day
                )

            # Si todavía no seleccionó ninguna fecha,
            # mostramos HOY como seleccionado visualmente.
            hoy = datetime.date.today()

            return (
                hoy.year == self.current_date.year
                and
                hoy.month == self.current_date.month
                and
                hoy.day == day
            )

    # ==========================================================
    # SUMAR MESES
    # ==========================================================

    def add_months(
        self,
        source_date,
        months
    ):

        month = (
            source_date.month
            - 1
            + months
        )

        year = (
            source_date.year
            + month // 12
        )

        month = (
            month % 12
            + 1
        )

        return datetime.date(
            year,
            month,
            1,
        )