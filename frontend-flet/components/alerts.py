import flet as ft
import asyncio


class Toast(ft.Container):

    def __init__(self):

        super().__init__()

        self.visible = False

        self.top = 20

        self.right = 20

        self.padding = 15

        self.border_radius = 12

        self.animate_opacity = 300

        self.bgcolor = "#DCFCE7"

        self.content = ft.Row(

            tight=True,

            controls=[

                ft.Icon(
                    ft.Icons.CHECK_CIRCLE,
                    color="#166534"
                ),

                ft.Text(
                    "",
                    color="#166534",
                    weight=ft.FontWeight.BOLD
                )
            ]
        )

    async def show(
        self,
        page,
        text,
        tipo="success",
        duration=5
    ):

        colores = {

            "success": {
                "bg": "#DCFCE7",
                "text": "#166534",
                "icon": ft.Icons.CHECK_CIRCLE
            },

            "error": {
                "bg": "#FEE2E2",
                "text": "#991B1B",
                "icon": ft.Icons.ERROR
            },

            "info": {
                "bg": "#DBEAFE",
                "text": "#1D4ED8",
                "icon": ft.Icons.INFO
            }
        }

        style = colores[tipo]

        self.bgcolor = style["bg"]

        self.content.controls[0].name = style["icon"]

        self.content.controls[0].color = style["text"]

        self.content.controls[1].value = text

        self.content.controls[1].color = style["text"]

        self.visible = True

        page.update()

        await asyncio.sleep(3)

        self.visible = False

        page.update()