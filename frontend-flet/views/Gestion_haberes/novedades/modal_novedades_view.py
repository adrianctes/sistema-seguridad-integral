import asyncio
from datetime import datetime

import flet as ft
import httpx
import calendar
from core.config import settings
from components.datapicker import DatePickerCustom
from core.constants import MODALIDAD_PAGO

from utils.formatters import filtrar_decimal, formatear_moneda,parsear_moneda

class ModalNovedad(ft.AlertDialog):

    def __init__(self, page, on_success=None):

        super().__init__(modal=True)

        self.page_ref = page
        self.on_success = on_success

        self.legajo_id = 0
        self.item_id = 0
        self.modalidad_pago_id = 0
        self.concepto_id = 0
    
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

        self.lbl_fecha_vigencia_novedad = ft.Text(
            "Vigencia de la novedad",
            size=12,
            weight=ft.FontWeight.BOLD
        )

        self.lbl_titulo_condicion = ft.Text(
            value="Condicion",
            size=12,
            weight=ft.FontWeight.BOLD
        )
        
        self.lbl_condicion = ft.Text(
            value="",
            size=12,
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
        self.cmb_legajo = ft.Dropdown(
            label="Legajo",
            hint_text="Seleccione un legajo",
            options=[],
            expand=True,
            on_select=lambda e: self.page_ref.run_task(
                        self.cambio_legajo
                    )
        )

        self.cmb_concepto = ft.Dropdown(
            label="Concepto",
            options=[],
            expand=True
        )

        self.fecha_desde = DatePickerCustom(
            self.page_ref,
            label="Fecha Desde"
        )

        self.fecha_hasta = DatePickerCustom(
            self.page_ref,
            label="Fecha Hasta"
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
            on_blur=self.formatear_valor
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
                            content=self.cmb_legajo
                        ),
                        ft.Container(
                             content=ft.Row(
                                    controls=[
                                        self.lbl_titulo_condicion,
                                        self.lbl_condicion,
                                    ],
                                    spacing=5,
                                )
                          
                        ),
                        ft.Container(
                            content=self.cmb_concepto
                        ),

                    
                    ft.Row(
                     self.lbl_fecha_vigencia_novedad
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                           
                            ft.Container(
                                expand=1,
                                content=self.fecha_desde
                            ),

                            ft.Container(
                                expand=1,
                                content=self.fecha_hasta
                            ),
                        ]
                    ),

                    ft.Row(
                        spacing=10,
                        controls=[

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

    async def abrir(self,  item=None):

        self.limpiar()
        await self.cargar_legajos()
        
        self.item_id = 0

        self.lbl_titulo_accion.value = "Agregar Nueva Novedad"
  
        if item:
            self.lbl_titulo_accion.value = "Editar Novedad"
            self.cmb_legajo.value = str(item["legajo_id"])
              
            self.item_id = item["id"]
            self.obtener_condicion()
            await self.cargar_conceptos()
            self.cmb_concepto.value = int(item["concepto_id"])
                  
            self.fecha_desde.set_value(item["fecha_desde"])
            self.fecha_hasta.set_value(item["fecha_hasta"])
            self.txt_cantidad.value = str(item["cantidad"])
            self.txt_valor.value = formatear_moneda(item["valor"])
           

            self.chk_activo.value = item.get(
                "activo",
                True
            )

        if self not in self.page_ref.overlay:
            self.page_ref.overlay.append(self)

        self.page_ref.dialog = self

        self.open = True

        self.page_ref.update()

    async def cargar_legajos(self):

        async with httpx.AsyncClient() as client:

            response = await client.get(

                f"{settings.URL_BACKEND}/legajos/activos",

                headers={
                    "Authorization": f"Bearer {settings.TOKEN}"
                }
            )

        if response.status_code != 200:
            return

        self.legajos = {}

        self.cmb_legajo.options = []

        for x in response.json():

            self.legajos[str(x["id"])] = x

            self.cmb_legajo.options.append(
                ft.dropdown.Option(
                    key=str(x["id"]),
                    text=f'{x["apellido"]}  {x["nombre"] }'
                )
            )

    async def cargar_conceptos(self):

        if not self.cmb_legajo.value:
            return

        legajo = self.legajos[self.cmb_legajo.value]

        self.legajo_id = legajo["id"]

        self.modalidad_pago_id = legajo["modalidad_pago_id"]


        async with httpx.AsyncClient() as client:

            response = await client.get(

                f"{settings.URL_BACKEND}/conceptos/modalidad-pago/{self.modalidad_pago_id}/novedades",

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

    def limpiar(self):

        self.item_id = 0

        self.cmb_legajo.value = None
        self.cmb_legajo.text= ""
        self.cmb_legajo.error_text= None

        self.cmb_concepto.value = None
        self.cmb_concepto.text = None
        self.cmb_concepto.error_text= None

        self.fecha_desde.reset()
        self.fecha_hasta.reset()
        self.fecha_desde.clear_error()
        self.fecha_hasta.clear_error()

        self.txt_cantidad.value = "1.00"

        self.txt_valor.value = "0.00"

        self.chk_activo.value = True

        self.lbl_mensaje.visible = False

        self.lbl_mensaje.value = ""

        self.lbl_titulo_accion.value = (
            "Agregar Nueva Novedad"
        )

    def cerrar(self, e=None):

        self.open = False

        self.page_ref.dialog = None

        self.page_ref.update()
    async def guardar(self, e):
        if not await self.validar_formulario():
            return

        self.loading.visible = True

        self.page_ref.update()
        
        fecha_hasta = self.calcular_ultimo_dia_del_mes()

        try:

            payload = {

                "legajo_id": self.legajo_id,
                "concepto_id":  self.cmb_concepto.value,
                "fecha_desde": self.fecha_desde.get_value(),
                "fecha_hasta": fecha_hasta,#self.fecha_hasta.get_value(),
                "cantidad" :float(self.txt_cantidad.value),
                "valor": parsear_moneda(self.txt_valor.value),
                "activo": self.chk_activo.value if self.chk_activo.value is not None else False
            }
      
            ok = False
            if self.item_id == 0 :
                ok = await self.api_crear(
                    payload
                )
            else :
               
                ok = await self.api_editar(
                    payload
                )


            if not ok:
                self.lbl_mensaje.value = (
                    "Ocurrio algun error al guardar."
                )

                self.lbl_mensaje.color = (
                    "#FF1707"
                )

                self.lbl_mensaje.visible = True

                self.page_ref.update()

                return


            self.lbl_mensaje.value = ("Guardado correctamente")

            self.lbl_mensaje.color = ("#15803D")

            self.lbl_mensaje.visible = True

            self.page_ref.update()

            await asyncio.sleep(0.8)

            self.cerrar()

            if self.on_success:

                await self.on_success()

        finally:

            self.loading.visible = False

            self.page_ref.update()

    async def validar_formulario(self):

            valido = True

            # Limpiar errores anteriores
            self.fecha_desde.error_text= None
            self.fecha_hasta.error_text = None
            self.txt_valor.error = None
            self.txt_cantidad.error = None

            if not self.cmb_legajo.value:
                self. cmb_legajo.error_text = "Seleccione legajo"
                print ("Error en elegajo")
                valido = False

            if self.item_id == 0 :    
                if not self.cmb_concepto.value:
                    self. cmb_concepto.error_text = "Seleccione concepto"
                    print ("Error en concepto")
                    valido = False
                

            if self.fecha_desde.get_value() is None:
       
                self.fecha_desde.set_error("Debe ingresar la fecha desde")
                print (f"Error en fechas desde {self.fecha_desde.value}")
                valido = False

           
            if  self.fecha_hasta.get_value() is None:
                self.fecha_hasta.set_error("Debe ingresar la fecha hasta")
                valido = False
                print (f"Error en fechas hasta {self.fecha_hasta.get_value()}")

            if (
                self.fecha_desde.get_value() 
                and self.fecha_hasta.get_value()
                and self.fecha_hasta.get_value()  < self.fecha_desde.get_value()
            ):
                self.fecha_hasta.set_error("Debe ser mayor o igual a la fecha desde")
       

            try:
                cantidad = float(self.txt_cantidad.value)
                if cantidad <= 0:
                    self.txt_cantidad.error = "Debe ser mayor a 0"
                    valido = False
            except (TypeError, ValueError):
                self.txt_cantidad.error = "Cantidad inválida"
                valido = False
            
            if not self.txt_valor.value:
                self.txt_valor.error = "Debe ingresar el valor"
                valido = False
       
            self.page_ref.update()
           
            return valido

    async def api_crear(self, data):
        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/novedades"

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

        url = f"{settings.URL_BACKEND}/novedades/{self.item_id}"

        async with httpx.AsyncClient() as client:

            response = await client.put(
                url,
                json=data,
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
       
        return response.status_code in (200, 201)            
    
    def solo_decimal(self, e):
            nuevo_valor = filtrar_decimal(e.control.value)

            if nuevo_valor != e.control.value:
                e.control.value = nuevo_valor
                e.control.update()
   
    def obtener_condicion(self):
        if not self.cmb_legajo.value:
            return False

        legajo = self.legajos[self.cmb_legajo.value]

        self.legajo_id = legajo["id"]

        self.modalidad_pago_id = legajo["modalidad_pago_id"]
     

        modalidad = next(
            (m for m in MODALIDAD_PAGO if m["id"] == self.modalidad_pago_id), None)

        self.lbl_condicion.value = modalidad["nombre"] if modalidad else ""

        return True

    async def cambio_legajo(self):

       if self.obtener_condicion():
            self.cmb_concepto.value = None

            await self.cargar_conceptos()

            self.page_ref.update()

    def calcular_ultimo_dia_del_mes(self):

        fecha_desde = self.fecha_desde.get_value()
        fecha_hasta = self.fecha_hasta.get_value()

        if fecha_hasta:
            return fecha_hasta

        if not fecha_desde:
            return None

        fecha_desde = datetime.strptime(
            fecha_desde,
            "%Y-%m-%d"
        ).date()

        ultimo_dia = calendar.monthrange(
            fecha_desde.year,
            fecha_desde.month
        )[1]

        return fecha_desde.replace(
            day=ultimo_dia
        ).strftime("%Y-%m-%d")
    
    def formatear_valor(self, e):
        try:
            valor = parsear_moneda(e.control.value)
            e.control.value = formatear_moneda(valor)
            e.control.error = None
        except ValueError:
            e.control.error = "Importe inválido"

        e.control.update()
