import flet as ft
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

    # =====================================
    # OPEN CALENDAR
    # =====================================

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

    # =====================================
    # BUILD CALENDAR
    # =====================================

    def build_calendar(self):

        year = self.current_date.year

        month = self.current_date.month

        cal = calendar.monthcalendar(
            year,
            month
        )

        # =====================================
        # HEADER
        # =====================================

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

        # =====================================
        # DAYS
        # =====================================

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

    # =====================================
    # SELECT DAY
    # =====================================

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

    # =====================================
    # NAVIGATION
    # =====================================

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
   