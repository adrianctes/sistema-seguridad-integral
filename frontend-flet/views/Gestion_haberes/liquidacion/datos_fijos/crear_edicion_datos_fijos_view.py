import asyncio
import calendar

import flet as ft

from components.datapicker import DatePickerCustom
from components.alerts import Toast
import httpx

from datetime import date, datetime, timedelta

from core.config import settings


class DatosFijosAltaEdicionView(ft.Container):

    def __init__(self, page, layout):

        super().__init__()
        self.page_ref = page
        self.layout = layout

        self.toast = Toast()

        self.id = 0

        self.expand = True

        self.bgcolor = "#F1F5F9"

        self.padding = 20
       
        self.estado =   "ABIERTO"

        self.periodo = None

        # =====================================
        # CONTROLES
        # =====================================
        self.loading = ft.ProgressRing(
            visible=False
        )
        
        self.lbl_titulo = ft.Text(
            value="Nuevo Datos Fijos de Liquidación",
            size=20,
            weight=ft.FontWeight.BOLD
        )

        self.txt_fecha = ft.TextField(
            label="Fecha",
            value=datetime.now().strftime("%d/%m/%Y"),
            read_only=True,
            expand=True,
            height=40,
            filled=True,
            bgcolor="#F8FAFC",
            border_color="#CBD5E1",
            text_size=12,
        )

        self.cmb_tipo_liquidacion = ft.Dropdown(
                        label="Tipo de Liquidación",
                        expand=True,
                        height=40,
                        #on_select=self.cambio_modalidad,
                        options=[
                            ft.dropdown.Option("1", "Normal"),
                            ft.dropdown.Option("2", "Sac"),
                            ft.dropdown.Option("3", "Complementaria"),
                            ft.dropdown.Option("4", "Especial"),
                        ]
                    )
        
        self.cmb_modalidad_liquidacion = ft.Dropdown(
                label="Modalidad de Liquidación",
                expand=True,
                height=40,
                value="MENSUAL",
                on_select=self.cambio_modalidad,
                options=[
                    ft.dropdown.Option("1", "Mensual"),
                    ft.dropdown.Option("2", "Quincenal"),
                    ft.dropdown.Option("3", "Semanal"),
                    ft.dropdown.Option("4", "Especial"),
                ]
            )

        self.txt_periodo = ft.TextField(
            label="Período de Liquidación",
            read_only=True,
            height=40,
            expand=True,
            filled=True,
            bgcolor="#F8FAFC",
            border_color="#CBD5E1",
        )

        self.txt_numero = ft.TextField(
            label="Numero",
            width=70,
            height=40,
            value="1",
            read_only=True,
            border_radius=0,
            border_color="#CBD5E1",
            filled=True,
        )

        self.fecha_desde = DatePickerCustom(
            page=self.page_ref,
            label="Fecha Desde",
            on_change=self.fecha_desde_change

        )
        self.fecha_desde.input.height = 40

        self.fecha_hasta = DatePickerCustom(
            page=self.page_ref,
            label="Fecha Hasta",
            on_change=self.fecha_hasta_change

        )
        self.fecha_hasta.input.height = 40

        self.cmb_periodo_pago = ft.Dropdown(
            label="Período de Pago",
            width=180,
            height=40,
            options=[]
        )

        self.fecha_pago = DatePickerCustom(
            page=self.page_ref,
            label="Fecha de Pago"
        )

        self.chk_abierto = ft.Checkbox(
            label="Abierto",
            value=True
        )

        self.content = self.build()
    
    def build(self):

        return ft.Stack(

            expand=True,

            controls=[

                ft.Column(

                    expand=True,

                    spacing=15,

                    controls=[

                        self.header(),

                        self.formulario(),
                      
                        self.footer()

                    ]

                ),

                self.toast

            ]

        )
    
    def header(self):

        return ft.Row(

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

            controls=[

                ft.Column(

                    spacing=2,

                    controls=[

                        self.lbl_titulo,

                        ft.Text(

                            "Complete los datos del formulario",

                            size=11,

                            color="#64748B"

                        ),
                      
                    ]

                ),     
                    ]

                )
    
    def formulario(self):

        return ft.Container(

            expand=True,

            bgcolor="white",

            padding=20,

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            content=ft.Column(

                spacing=20,

                controls=[
                    ft.Row(
                            spacing=10,
                            controls=[
                                ft.Container(
                                    expand=1,
                                    content=self.txt_fecha,
                                ),

                                ft.Container(
                                    expand=1,
                                    content=self.cmb_tipo_liquidacion,
                                ),

                                ft.Container(
                                    expand=1,
                                    content=self.cmb_modalidad_liquidacion,
                                ),
                            ],
                        ),

                    ft.Row(

                        controls=[

                            ft.Container(
                                expand=1,
                                content=self.fecha_desde
                            ),

                            ft.Container(
                                expand=1,
                                content=self.fecha_hasta
                            )

                        ]

                    ),

                    ft.Row(

                        controls=[

                            ft.Container(
                                expand=1,
                                content=self.txt_periodo
                            ),
                            ft.Container(
                                expand=1,
                                content=self.txt_numero
                            )
                        
                            
                        ]

                    ),
                    
                    ft.Row(

                        controls=[
                            self.chk_abierto
                        ]
                        )


                ]

            )

        )
    
    def footer(self):

            self.btn_guardar = ft.FilledButton(
                "Guardar",
                on_click=self.guardar,
                disabled=False,
                style=ft.ButtonStyle(
                    bgcolor={
                        ft.ControlState.DEFAULT: "#030B16",
                        ft.ControlState.DISABLED: "#9CA3AF",
                    },
                    color={
                        ft.ControlState.DEFAULT: "white",
                        ft.ControlState.DISABLED: "#E5E7EB",
                    }
                )
               
            )

            return ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    self.loading,

                    ft.OutlinedButton(
                        "Cancelar",
                        on_click=self.cancelar
                    ),

                    self.btn_guardar
                ],
            )
    
    async def set_mode(self, id):

        self.id = id

        if id == 0:

            self.nuevo()

        else:
            self.lbl_titulo.value = "Editar  Datos Fijos de Liquidación"
            await self.cargar(id)

        if self.estado =="CERRADO":
            self.btn_guardar.disabled = True    


    def cambio_modalidad(self, e):
        modalidad = self.cmb_modalidad_liquidacion.text
        self.fecha_desde.reset()
        self.fecha_hasta.reset()
        self.txt_periodo.value= None
        self.txt_periodo.value= ""
       
    
        self.page_ref.update()


        if modalidad == "ESPECIAL":

            self.fecha_desde.input.read_only = False
            self.fecha_hasta.input.read_only = False

        else:

            self.fecha_desde.input.read_only = True
            self.fecha_hasta.input.read_only = True

            if self.fecha_desde.selected_date:

                self.fecha_desde_change(
                    self.fecha_desde.selected_date
                )

    def fecha_desde_change(self, fecha):

        if not fecha:
            return

        modalidad = self.cmb_modalidad_liquidacion.text

        if modalidad == "Mensual":

            ultimo = calendar.monthrange(
                fecha.year,
                fecha.month
            )[1]

            self.fecha_hasta.set_value(
                date(fecha.year, fecha.month, ultimo)
            )

        elif modalidad == "Quincenal":

            self.fecha_hasta.set_value(
                fecha + timedelta(days=14)
            )

        elif modalidad == "Semanal":

            self.fecha_hasta.set_value(
                fecha + timedelta(days=6)
            )

        self.calcular_periodo()

    def fecha_hasta_change(self, fecha):

     self.calcular_periodo()
    
    def calcular_periodo(self):

        desde = self.fecha_desde.selected_date
        hasta = self.fecha_hasta.selected_date
       
        if not desde or not hasta:

            self.txt_periodo.value = ""
            self.page_ref.update()
            return

        modalidad = self.cmb_modalidad_liquidacion.text
    

        if modalidad == "Mensual":
            self.txt_numero.value = 1
            self.periodo = (
               f"{desde.strftime('%Y%m')}"
            )
            self.txt_periodo.value = (
                desde.strftime("%m/%Y")
            )

        elif modalidad == "Quincenal":

            numero = 1 if desde.day <= 15 else 2
            self.txt_numero.value = numero

            self.periodo = (
               f"{desde.strftime('%Y%m')}"
            )


            self.txt_periodo.value = (
                f"{desde.strftime('%m/%Y')}"
            )

        elif modalidad == "Semanal":

            numero_semana = ((desde.day - 1) // 7) + 1
            self.txt_numero.value = numero_semana

            self.periodo = (
                 f"{desde.strftime('%Y%m')}"
            )

            self.txt_periodo.value = (
                  f"{desde.strftime('%m/%Y')}"
            )

        else:

            self.txt_periodo.value = (
                f"{desde.strftime('%d/%m/%Y')} "
                f"al "
                f"{hasta.strftime('%d/%m/%Y')}"
            )

       
        self.page_ref.update()

    def nuevo(self):

        self.id = 0


        self.fecha_desde.reset()

        self.fecha_hasta.reset()

        self.fecha_pago.reset()

        self.txt_numero.value = None

        self.cmb_tipo_liquidacion.value = None
        self.cmb_tipo_liquidacion.text = ""
        self.cmb_modalidad_liquidacion.value = None
        self.cmb_modalidad_liquidacion.text =""
        self.cmb_periodo_pago.value = None

        self.txt_periodo.value = ""

        self.chk_abierto.value = True

        self.page_ref.update()

    async def cancelar(self, e=None):
        self.page_ref.layout.change_view(
            "datos_fijos_liquidacion"
        )
    
    async def cargar(self, id):

        token = settings.TOKEN

        headers = {

            "Authorization": f"Bearer {token}"

        }

        url = f"{settings.URL_BACKEND}/datos-fijos-liquidacion/{id}"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(

                    url,

                    headers=headers

                )

            if response.status_code != 200:

                await self.toast.show(

                    self.page_ref,

                    "No se pudo cargar el registro",

                    "error"

                )

                return

            item = response.json()

            self.txt_fecha.value = datetime.fromisoformat(
                 item["fecha_carga"]
            ).strftime("%d/%m/%Y")
            self.fecha_desde.set_value(item["fecha_desde"])

            self.fecha_hasta.set_value(item["fecha_hasta"])

           # self.fecha_pago.set_value(

            #    datetime.strptime(

             #       item["fecha_pago"],

              #     "%Y-%m-%dT%H:%M:%S"

               # ).date()

            #)
            self.cmb_tipo_liquidacion.value = item["tipo_liquidacion_id"]
            self.cmb_modalidad_liquidacion.value = item["modalidad_liquidacion_id"]

            self.txt_numero.value =  item["numero"]

 #           self.cmb_periodo_pago.value = item["periodo_pago"]

            self.txt_periodo.value =  f"{str(item['periodo'])[4:6]}/{str(item['periodo'])[:4]}"
            self.periodo = item['periodo']

            self.estado=item["estado"] 

            self.chk_abierto.value = item["estado"] == "ABIERTO"

            self.page_ref.update()

        except Exception as ex:

            print(ex)

            await self.toast.show(

                self.page_ref,

                str(ex),

                "error"

            )
    
    async def guardar(self, e):


        if not await self.validar_formulario():
            return

        self.loading.visible = True

        self.page_ref.update()

        payload = {
            "fecha_carga":   datetime.strptime(self.txt_fecha.value, "%d/%m/%Y").strftime("%Y-%m-%d"),
            "periodo": self.periodo,
            "numero" : self.txt_numero.value,
            "fecha_desde": self.fecha_desde.get_value(),
            "fecha_hasta": self.fecha_hasta.get_value(),
            "modalidad_liquidacion_id": int(self.cmb_modalidad_liquidacion.value),
            "tipo_liquidacion_id" : int(self.cmb_tipo_liquidacion.value),
            "estado": "Abierto" if self.chk_abierto.value else "Cerrado"
            #"periodo_pago": self.txt_periodo_pago.value,
            #"fecha_pago": self.fecha_pago.get_value(),
        }
       
        ok = False
        if self.id == 0 :
                ok = await self.api_crear(
                    payload
                )
        else :
               
                ok = await self.api_editar(
                    payload
                )


        if not ok:
                self.loading.visible = False
               
                await self.toast.show(
                    self.page_ref,
                     "ocurrio un error al guardar",
                    "error"
                ) 
  
             

                self.page_ref.update()

                return
        
        await self.toast.show(
                    self.page_ref,
                     "Los datos se guardaron corectamente",
                    "success"
                )

        self.page_ref.update()
      
        await asyncio.sleep(1)

        self.page_ref.layout.change_view(
                    "datos_fijos_liquidacion"
                )
        self.loading.visible = False
        return

    async def validar_formulario(self):

        valido = True

        # Fecha
        if not self.txt_fecha.value:
            self.fecha.error_text = "Debe ingresar la fecha."
            valido = False
        else:
            self.txt_fecha.error_text = None

        # Período
        if not self.txt_periodo.value:
            self.txt_periodo.error_text = "Debe ingresar el período."
            valido = False
        else:
            self.txt_periodo.error_text = None

        # Fecha desde
        if not self.fecha_desde.get_value():
            self.fecha_desde.error_text = "Debe ingresar la fecha desde."
            valido = False
        else:
            self.fecha_desde.error_text = None

        # Fecha hasta
        if not self.fecha_hasta.get_value():
            self.fecha_hasta.error_text = "Debe ingresar la fecha hasta."
            valido = False
        else:
            self.fecha_hasta.error_text = None

        # Modalidad de liquidación
        if not self.cmb_modalidad_liquidacion.value:
            self.cmb_modalidad_liquidacion.error_text = "Debe seleccionar una modalidad de liquidación."
            valido = False
        else:
            self.cmb_modalidad_liquidacion.error_text = None

        

        self.page_ref.update()

        return valido
    
    async def api_crear(self,  data):
        
        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/liquidaciones/datos-fijos"
        
        async with httpx.AsyncClient(timeout=30.0) as client:

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

        url = f"{settings.URL_BACKEND}/datos-fijos-liquidacion/{self.id}"

        async with httpx.AsyncClient() as client:

            response = await client.put(
                url,
                json=data,
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
       
        return response.status_code in (200, 201)            
    