import asyncio
import flet as ft
import httpx

from components.alerts import Toast
from core.config import settings

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
            height=55,
            max_length=6,
            on_change=self.force_upper
        )

        self.txt_nombre = ft.TextField(
            label="Descripcion",
            border_radius=0,
            expand=True,
            height=55,
            max_length=60,
        )

        self.txt_orden = ft.TextField(
            label="Orden impresion",
            border_radius=0,
            height=55,
            max_length=10,
        )

        self.txt_abreviatura = ft.TextField(
            label="Abreviatura",
            border_radius=0,
            expand= True,
            height=55,
            max_length=10,
            on_change=self.force_upper
        )

        self.txt_secuencia = ft.TextField(
            label="Secuencia",
            border_radius=0,
            expand= True,
            height=55,
            max_length=10,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.solo_numeros
        )

        self.cmb_unidad_medida = ft.Dropdown(
            label="Unidad de medida",
            border_radius=0,
            expand=True,
            height=35,
            value="IMPORTE",
            options=[
                ft.dropdown.Option("DIA"),
                ft.dropdown.Option("HORA"),
                ft.dropdown.Option("IMPORTE")
            ]
        )
        
        self.cmb_tipo_calculo = ft.Dropdown(

                label="Tipo",

                expand=True,

                height=40,

                value = "FIJO",

                border_radius=0,
                margin=ft.Margin(0, -15, 0, 0),

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
            height=30,
            options=[]
        )

        self.txt_formula = ft.TextField(
            label="Fórmula",
            height=55,
            multiline=True,
            min_lines=1,
            max_lines=1,
            visible=False,
            expand=True,
            border_radius=0,
            max_length=100
        )
        self.chk_novedad = ft.Checkbox(label="Es novedad", value=False)
        self.chk_activo = ft.Checkbox(label="Activo", value=True)
        self.container_codigo = ft.Container(
            expand=1,
            content=self.txt_codigo,
            visible=False
        )
        self.container_abreviatura = ft.Container(
            expand=1,
            content=self.txt_abreviatura
        )

        self.container_secuencia = ft.Container(
                    expand=1,
                    content=self.txt_secuencia
                )
        self.container_orden = ft.Container(
                    expand=1,
                    content=self.txt_orden
                )
        self.container_unidad_medida = ft.Container(
                            expand=1,
                            content=self.cmb_unidad_medida,
                            margin=ft.Margin(0, -15, 0, 0),
                            )
        self.container_formula = ft.Container(
                    expand=3,
                    content=self.txt_formula
                )
    
               
        self.fila_1= ft.Row(
            controls=[
                self.container_codigo,
                self.container_abreviatura,
            ]
        )
        self.fila_3 = ft.Row(
                            controls=[
                                self.container_secuencia,
                                self.container_orden,
                                self.container_unidad_medida
                            ]
                        )
        self.fila_4= ft.Row(
                    controls=[
                        self.cmb_tipo_calculo,
                        self.container_formula,
                    ]
                )
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
                            self.fila_1,

                            ft.Row([
                                     ft.Container(expand=3, content=self.txt_nombre)
                                    ]),
                            self.fila_3,  
                            self.fila_4,

                            #  ft.Row([
                            #    ft.Container(expand=1, content=self.cmb_tipo_calculo),
                            #    ft.Container(expand=2, content=self.txt_formula)
                            #]), 


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
      
        #visible = (
        #    e.control.value == "FORMULA"
        #)
        #self.txt_formula.visible = visible

        #self.content.controls[0] = self.build()
        self.txt_formula.visible = (
            self.cmb_tipo_calculo.value == "FORMULA"
        )
        self.page_ref.update()
       

    def force_upper(self, e):
        e.control.value = (e.control.value or "").upper()
        e.control.update()

    def solo_numeros(self, e):

        limpio = "".join(
            filter(str.isdigit, e.control.value or "")
        )

        if e.control.value != limpio:

            e.control.value = limpio
            e.control.update()

    async def set_mode(self, concepto_id: int):
        self.limpiar()
        self.concepto_id = concepto_id
        
        if concepto_id == 0:
            self.titulo_accion = "Nuevo Concepto"
            self.lbl_titulo_accion.value = self.titulo_accion
            self.container_codigo.visible = False
            self.container_secuencia.visible= False
                       
        else:
            item = await self.obtener_concepto_by_id(concepto_id)

            if item:
                self.editar(item)
                self.container_codigo.visible = True
                self.container_secuencia.visible= True

        #self.page_ref.update()        

         
    async def load(self):
        await self.cargar_clasificaciones()

    async def cargar_clasificaciones(self):

        try:
            token = self.page.session.store.get("access_token")
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.URL_BACKEND}/clasificacion-conceptos",
                    headers={"Authorization": f"Bearer {token}"}
                )

            if response.status_code != 200:
                return

            datos = response.json()

            self.cmb_clasificacion.options = [
                ft.dropdown.Option(str(x["id"]), x["nombre"])
                for x in datos
            ]
            if self.cmb_clasificacion.options:
                self.cmb_clasificacion.value = self.cmb_clasificacion.options[0].key
            self.cmb_clasificacion.update()
            

        except Exception as ex:
            await self.toast.show(self.page_ref, str(ex), "error")

    async def obtener_concepto_by_id(self, id: int):

        token = self.page_ref.session.store.get("access_token")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.URL_BACKEND}/conceptos/{id}",
                headers={"Authorization": f"Bearer {token}"}
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
            "abreviatura"  : data.get("abreviatura"),
            "secuencia"  : data.get("secuencia"),
            "unidad_medida"  : data.get("unidad_medida")

        }

    def editar(self, item):
   
        self.titulo_accion = "Editar Concepto"
        self.lbl_titulo_accion.value = self.titulo_accion

        self.concepto_id = item["id"]

        self.txt_codigo.value = item["codigo"]
        self.txt_nombre.value = item["nombre"]

        self.txt_abreviatura.value =  item["abreviatura"]
        self.cmb_unidad_medida.value =  item["unidad_medida"]
        self.txt_secuencia.value =  item["secuencia"] 

        self.cmb_tipo_calculo.value = item["tipo_calculo"]
        self.cmb_clasificacion.value = item["clasificacion_concepto_id"]

        self.txt_formula.value = item.get("formula") or ""
        self.txt_formula.visible = item["tipo_calculo"] == "FORMULA"

        self.chk_novedad.value = item["es_novedad"]
        self.chk_activo.value = item["activo"]

        self.txt_orden.value =  item["orden"] or ""

    def limpiar(self):

        self.concepto_id = 0

        self.lbl_titulo_accion.value = "Nuevo Concepto"

        self.txt_codigo.value = ""
        self.container_codigo.visible = False

        self.txt_nombre.value = ""
        self.txt_nombre.error = ""
        self.txt_nombre.error = None
     
        self.txt_orden.value = ""

        self.txt_abreviatura.value = ""
        self.txt_abreviatura.error= ""
        self.txt_abreviatura.error = None
       
        self.txt_secuencia.value =""
        self.txt_secuencia.error =""
        self.txt_secuencia.error = None
               
        self.txt_orden.value = ""
            

        self.txt_formula.value = ""
        self.txt_formula.visible = False

        self.chk_novedad.value = False

        self.chk_activo.value = True


        self.page_ref.update()

    async def guardar(self, e):
        if not await self.validar_formulario():
            return
        
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
                "secuencia": self.txt_secuencia.value,
                "abreviatura": self.txt_abreviatura.value,
                "unidad_medida" : self.cmb_unidad_medida.value
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
            else:
                await self.toast.show(
                   self.page,
                    "Error al guardar",
                   "error"
                )
        

        finally:
            self.loading.visible = False
            self.page_ref.update()

    async def api_crear(self, data):
    
        token = self.page_ref.session.store.get("access_token")

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

        token = self.page_ref.session.store.get("access_token")

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

    async def validar_formulario(self):
    
            valido = True
    
            if  self.concepto_id !=0:
                if  not self.txt_codigo.value:
                    self.txt_codigo.error = "Debe ingresar codigo."
                    valido = False
                else:
                    self.txt_codigo.error = None
    
            
            if not self.txt_abreviatura.value:
                self.txt_abreviatura.error = "Debe ingresar abreviatura."
                valido = False
            else:
                self.txt_abreviatura.error = None

            if not self.txt_nombre.value:
                self.txt_nombre.error = "Debe ingresar descripcion."
                valido = False
            else:
                self.txt_nombre.error = None
            
            if self.concepto_id != 0:
                if not self.txt_secuencia.value:
                    self.txt_secuencia.error = "Debe ingresar secuencia."
                    valido = False
                else:
                    self.txt_secuencia.error = None

           
            if self.cmb_tipo_calculo.value =="FORMULA": 
                if not self.txt_formula.value:
                    self.txt_formula.error = "Debe ingresar formula."
                    valido = False
                else:
                    self.txt_formula.error = None

            self.page_ref.update()
            
            return valido