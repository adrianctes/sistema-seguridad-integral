import asyncio
import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings
from core.constants import MODALIDAD_PAGO

class CrearEditarConceptoView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.page_ref = page
        self.toast = Toast()

        self.concepto_id = 0

        self.expand = True
        self.bgcolor = "#F1F5F9"
        self.padding = 20
        self.loading = ft.ProgressRing(visible=False)
        self.titulo_accion = "Nuevo Concepto"
        self.lbl_titulo_accion = ft.Text(
           self.titulo_accion,
            size=18,
            weight=ft.FontWeight.BOLD
        )

        # ==========================
        # CAMPOS
        # ==========================
        self.txt_codigo = ft.TextField(
            label="Código",
            border_radius=0,
            expand=True,
            height=60,
            max_length=6,
            on_change=self.force_upper
        )

        self.txt_nombre = ft.TextField(
            label="Nombre",
            border_radius=0,
            expand=True,
            height=60,
            max_length=60,
        )

        self.txt_orden = ft.TextField(
            label="Orden",
            border_radius=0,
            height=40
        )
        
        self.cmb_tipo_calculo = ft.Dropdown(

                label="Tipo",

                expand=True,

                height=40,

                border_radius=0,

                options=[

                    ft.dropdown.Option("FIJO"),

                    ft.dropdown.Option("FORMULA"),

                    ft.dropdown.Option("PORCENTAJE")
                ]
            )
        # ✔ evento asignado después
        self.cmb_tipo_calculo.on_select = self.on_tipo_change

        self.cmb_clasificacion = ft.Dropdown(
            label="Clasificación",
            border_radius=0,
            expand=True,
            options=[]
        )

        self.txt_formula = ft.TextField(
            label="Fórmula",
            height=40,
            multiline=True,
            min_lines=1,
            max_lines=1,
            visible=False,
            expand=True,
            border_radius=0,
        )
        self.cmb_modalidad_pago = ft.Dropdown(
            label="Modalidad de pago",
            expand=True,
            height=55,
            options=[],
        )
        self.chk_novedad = ft.Checkbox(label="Es novedad", value=False)
        self.chk_activo = ft.Checkbox(label="Activo", value=True)

        self.content = ft.Stack(
            expand=True,
            controls=[
                self.build(),
                self.toast
            ]
        )

        page.run_task(self.load)
        
    def build(self):
        return ft.Column(
            expand=True,
            spacing=12,
            controls=[

                self.lbl_titulo_accion,

                ft.Container(
                    expand=True,
                    bgcolor="white",
                    border=ft.Border.all(1, "#E2E8F0"),
                    padding=20,
                    content=ft.Column(
                        spacing=18,
                        controls=[
                            ft.Row(
                                ft.Container(
                                            expand=1,
                                             content=self.cmb_modalidad_pago
                                        )
                            ),

                            ft.Row([
                                ft.Container(expand=1, content=self.txt_codigo),
                                ft.Container(expand=3, content=self.txt_nombre),
                            ]),

                           ft.Row([
                                ft.Container(expand=1, content=self.txt_orden),
                                ft.Container(expand=1, content=self.cmb_tipo_calculo),
                                ft.Container(expand=2, content=self.txt_formula),
                            ]),
                           
                            self.cmb_clasificacion,

                            ft.Row([
                                self.chk_novedad,
                                self.chk_activo
                            ]),

                            ft.Divider(),

                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    self.loading,

                                    ft.OutlinedButton(
                                        "Cancelar",
                                        on_click=lambda e: self.page_ref.layout.change_view("conceptos")
                                    ),

                                    ft.FilledButton(

                                        "Guardar",

                                        on_click=self.guardar,

                                        style=ft.ButtonStyle(
                                            bgcolor="#030B16",
                                            color="white"
                                        )
                                    ),
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    def on_tipo_change(self, e):
      
        visible = (
            e.control.value == "FORMULA"
        )
        self.txt_formula.visible = visible

        self.content.controls[0] = self.build()

        self.content.update()

    def force_upper(self, e):
        e.control.value = (e.control.value or "").upper()
        e.control.update()

    async def set_mode(self, concepto_id:int ):

            self.limpiar()

            self.concepto_id = concepto_id

           
            if concepto_id == 0:
               self.titulo_accion = "Nuevo Concepto"
               self.lbl_titulo_accion.value = self.titulo_accion
               return

            item = await self.obtener_concepto_by_id(concepto_id)

            if item:
                self.editar(item)

    async def load(self):
        await self.cargar_clasificaciones()
        await self.cargar_modalidad_pago()

    async def cargar_clasificaciones(self):

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.URL_BACKEND}/clasificacion-conceptos",
                    headers={"Authorization": f"Bearer {settings.TOKEN}"}
                )

            if response.status_code != 200:
                return

            datos = response.json()

            self.cmb_clasificacion.options = [
                ft.dropdown.Option(str(x["id"]), x["nombre"])
                for x in datos
            ]

            self.cmb_clasificacion.update()

        except Exception as ex:
            await self.toast.show(self.page_ref, str(ex), "error")

    async def obtener_concepto_by_id(self, id: int):

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.URL_BACKEND}/conceptos/{id}",
                headers={"Authorization": f"Bearer {settings.TOKEN}"}
            )

        if response.status_code != 200:
            await self.toast.show(self.page_ref, "Error API", "error")
            return None

        data = response.json()

        return {
            "id": data.get("id"),
            "codigo": data.get("codigo", ""),
            "nombre": data.get("nombre", ""),
            "tipo_calculo": data.get("tipo_calculo", ""),
            "clasificacion_concepto_id": data.get("clasificacion_concepto_id"),
            "es_novedad": data.get("es_novedad", False),
            "activo": data.get("activo", True),
            "formula": data.get("formula"),
            "orden" : data.get("orden"),
            "modalidad_pago_id" : data.get("modalidad_pago_id")
        }

    def editar(self, item):

        self.titulo_accion = "Editar Concepto"
        self.lbl_titulo_accion.value = self.titulo_accion

        self.concepto_id = item["id"]

        self.txt_codigo.value = item["codigo"]
        self.txt_nombre.value = item["nombre"]

        self.cmb_tipo_calculo.value = item["tipo_calculo"]
        self.cmb_clasificacion.value = item["clasificacion_concepto_id"]

        self.txt_formula.value = item.get("formula") or ""
        self.txt_formula.visible = item["tipo_calculo"] == "FORMULA"

        self.chk_novedad.value = item["es_novedad"]
        self.chk_activo.value = item["activo"]

        self.cmb_modalidad_pago.value = item["modalidad_pago_id"] 
        self.txt_orden.value =  item["orden"] or ""

   
        self.page_ref.update()

    def limpiar(self):

        self.concepto_id = 0

        self.lbl_titulo_accion.value = "Nuevo Concepto"

        self.txt_codigo.value = ""

        self.txt_nombre.value = ""

        self.txt_orden.value = ""

        self.cmb_tipo_calculo.value = ""
        self.cmb_tipo_calculo.selected_index = None

        self.cmb_clasificacion.value = ""
        self.cmb_clasificacion.selected_index = None

        self.cmb_modalidad_pago.value = ""
        self.cmb_modalidad_pago.selected_index = None

        self.txt_formula.value = ""

        self.txt_formula.visible = False

        self.chk_novedad.value = False

        self.chk_activo.value = True

        self.page_ref.update()
    async def cargar_modalidad_pago(self):
        self.cmb_modalidad_pago.options = [

                *[
                    ft.dropdown.Option(
                        key=str(item["id"]),
                        text=item["nombre"]
                    )

                    for item in MODALIDAD_PAGO
                ],

                ft.dropdown.Option(
                    key="0",
                    text="Todas"
                )
            ]
          
    async def guardar(self, e):
        try:
            self.loading.visible = True
            self.page_ref.update()

            data = {
                "codigo": self.txt_codigo.value,
                "nombre": self.txt_nombre.value,
                "orden": int(self.txt_orden.value or 0),
                "tipo_calculo": self.cmb_tipo_calculo.value,
                "clasificacion_concepto_id": int(self.cmb_clasificacion.value) if self.cmb_clasificacion.value else None,
                "formula": self.txt_formula.value if self.cmb_tipo_calculo.value == "FORMULA" else None,
                "es_novedad": self.chk_novedad.value,
                "activo": self.chk_activo.value,
                "modalidad_pago_id": self.cmb_modalidad_pago.value,
            }
          
            statu_code = False
         
            if self.concepto_id == 0:
               statu_code = await self.api_crear(data)
            else:
                statu_code = await self.api_editar(data)
       
            if statu_code:
                await self.toast.show(self.page_ref, "Guardado exitoso", "success")
                await asyncio.sleep(1)
                vista = self.page_ref.layout.views["conceptos"]
                await vista.reload_view()
                self.page_ref.layout.change_view("conceptos")

        finally:
            self.loading.visible = False
            self.page_ref.update()

    async def api_crear(self, data):

        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/conceptos"

        async with httpx.AsyncClient() as client:

            response = await client.post(
                url,
                json=data,
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        return response.status_code in (200, 201)        
    
    async def api_editar(self, data):

        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/conceptos/{self.concepto_id}"

        async with httpx.AsyncClient() as client:

            response = await client.put(
                url,
                json=data,
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        return response.status_code in (200, 201)