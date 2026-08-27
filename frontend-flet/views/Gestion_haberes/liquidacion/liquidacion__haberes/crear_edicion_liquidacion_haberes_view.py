import asyncio
from decimal import Decimal
import flet as ft
from datetime import datetime
import httpx
from core.config import settings
from components.alerts import Toast
from  core.config import settings
from utils.formatters import formatear_fecha

class LiquidacionHaberesAltaEdicionView(ft.Container):

    def __init__(self, page):

        super().__init__()

        self.toast = Toast()

        self.page_ref = page

        self.expand = True

        self.bgcolor = "#F8FAFC"

        self.padding = 10

        self.datos_fijos = {}

        self.modalidad_liquidacion_id =0

        self.legajos = {}

        self.resultado_liquidacion = None
 
        # =====================================================
        # CONTROLES
        # =====================================================

        self.loading = ft.Container(

                visible=False,

                expand=True,

                alignment=ft.Alignment.CENTER,

                bgcolor=ft.Colors.with_opacity(
                    0.30,
                    ft.Colors.BLACK,
                ),

                content=ft.Column(

                    tight=True,

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.ProgressRing(),

                        ft.Text(
                            "Liquidando...",
                            color="white",
                        ),

                    ],
                ),
            )

        self.lista_conceptos = ft.ListView(
            expand=True,
            spacing=0,
            auto_scroll=False
        )

        self.txt_fecha = ft.TextField(

            label="Fecha",
            text_size=14,
            value=datetime.now().strftime("%d/%m/%Y"),

            read_only=True,

            width=130,

            height=30,

            filled=True,

            border_radius=0,

            border_color="#CBD5E1"

        )

        self.cmb_datos_fijos = ft.Dropdown(

            label="Datos Fijos",
            text_size=10,
            expand=True,

            height=30,

            filled=True,

            border_radius=0,

            border_color="#CBD5E1",

            options=[],

            on_select=self.cambio_datos_fijos
        )

        self.cmb_legajos= ft.Dropdown(

            label="Legajo",
            text_size=10,
            expand=True,  

            height=30,

            filled=True,

            border_radius=0,

            border_color="#CBD5E1",

            options=[],

            on_select=self.cambio_legajo

        )

        # =====================================================
        # DATOS DEL LEGAJO
        # =====================================================

        self.lbl_apellido = ft.Text("-", size=11)

        self.lbl_nombre = ft.Text("-", size=11)

        self.lbl_cuil = ft.Text("-", size=11)

        self.lbl_cuil = ft.Text("-", size=11)

        self.lbl_categoria = ft.Text("-", size=11)

        self.lbl_modalidad = ft.Text("-", size=11)

        self.lbl_empresa = ft.Text("-", size=11)

        self.lbl_fecha_ingreso_actual = ft.Text("-", size=11)

        # =====================================================
        # BOTONES
        # =====================================================

        self.btn_liquidar = ft.FilledButton(

            "Liquidar",

            icon=ft.Icons.CALCULATE,

            width=130,

            height=30,

            style=ft.ButtonStyle(

                bgcolor="#030B16",

                shape=ft.RoundedRectangleBorder(radius=0)

            ),

            on_click=self.liquidar

        )

        self.btn_aceptar = ft.FilledButton(

            "Aceptar",

            icon=ft.Icons.SAVE,

            width=130,

            height=30,

            style=ft.ButtonStyle(

                bgcolor="#030B16",

                shape=ft.RoundedRectangleBorder(radius=0)

            ),

            on_click=self.aceptar

        )

        self.btn_cancelar = ft.OutlinedButton(

            "Cancelar",

            icon=ft.Icons.CLOSE,

            width=130,

            height=30,

            style=ft.ButtonStyle(

                shape=ft.RoundedRectangleBorder(radius=0)

            ),

            on_click=self.cancelar

        )

        # =====================================================
        # TOTALES
        # =====================================================

        self.lbl_total_haberes = ft.Text(

            "$ 0,00",

            weight=ft.FontWeight.BOLD,

            size=15

        )

        self.lbl_total_retenciones = ft.Text(

            "$ 0,00",

            weight=ft.FontWeight.BOLD,

            size=15

        )

        self.lbl_neto = ft.Text(

            "$ 0,00",

            weight=ft.FontWeight.BOLD,

            size=18,

            color="green"

        )

        # =====================================================
        # CONTENIDO
        # =====================================================

        self.content = self.build()
   

    """  def build(self):

        return ft.Container(

            expand=True,

            bgcolor="#F8FAFC",

            padding=10,

          

            content=ft.Column(

            expand=True,
  
            spacing=15,
        
            
            controls=[

                # =====================================
                # HEADER
                # =====================================

                ft.Row(

                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                    controls=[

                        ft.Column(

                            spacing=2,

                            controls=[

                                ft.Text(
                                    "Liquidacion de haberes",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color="#0F172A"
                                ),

                                ft.Text(
                                    "Nueva liquidacion",
                                    size=11,
                                    color="#64748B",
                                ),
                            ],
                        ),

                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=lambda e:
                                self.page_ref.layout.change_view(
                                    "liquidacion_haberes"
                                )
                        ),
                    ],
                ),

                    self.encabezado(),

                    self.datos_legajo(),

                    self.botonera(),

                    self.grilla(),

                    self.totales(),

                   
                ]

            )

        ) """
        
    def encabezado(self):

        return ft.Container(

            bgcolor="white",

            padding=10,

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            content=ft.Row(

                spacing=10,

                vertical_alignment=ft.CrossAxisAlignment.END,

                controls=[

                    ft.Container(
                        width=140,
                        content=self.txt_fecha
                    ),

                    ft.Container(
                        expand=2,
                        content=self.cmb_datos_fijos
                    ),

                    ft.Container(
                        expand=2,
                        content=self.cmb_legajos
                    )

                ]

            )

        )

    async def load(self):


        await self.buscar_datos_fijos_abiertos()

        await self.cargar_datos_fijos()

       
    def limpiar_controles(self):

            # Datos fijos
            #self.cmb_datos_fijos.text = ""
           #self.cmb_datos_fijos.value = None
           

            # Legajos
            self.cmb_legajos.text =""
            self.cmb_legajos.value = None
            self.cmb_legajos.options.clear()

            self.legajos = []

            self.modalidad_liquidacion_id = 0


            # Datos del legajo
            self.lbl_apellido.value = "-"
            self.lbl_nombre.value = "-"
            self.lbl_cuil.value = "-"
            self.lbl_categoria.value = "-"
            self.lbl_modalidad.value = "-"
            self.lbl_empresa.value = "-"
            self.lbl_fecha_ingreso_actual.value = "-"


            # Detalle liquidación
            self.lista_conceptos.controls.clear()


            # Totales
            self.lbl_total_haberes.value = "$ 0,00"
            self.lbl_total_retenciones.value = "$ 0,00"
            self.lbl_neto.value = "$ 0,00"

    
    async def cargar_datos_fijos(self):

        for item in self.datos_fijos:
            periodo=  f"{str(item['periodo'])[4:6]}/{str(item['periodo'])[:4]}"
            leyenda = f"{periodo} - {item['modalidad_liquidacion']}/{item['numero']}"
            self.cmb_datos_fijos.options.append(
                ft.dropdown.Option(
                    key=str(item["id"]),
                    text=leyenda
                )
            )
 
            self.page_ref.update()

    async def buscar_datos_fijos_abiertos(self):
            params = {}
            params["estado"] = "ABIERTO"      
    
            token = settings.TOKEN
    
            if not token:
    
                await self.toast.show(
                    self.page_ref,
                    "Sesión expirada",
                    "error"
                )
    
                return
    
            headers = {
                "Authorization": f"Bearer {token}"
            }
    
            url = f"{settings.URL_BACKEND}/datos-fijos-liquidacion"
    
            try:
    
                async with httpx.AsyncClient() as client:
    
                    response = await client.get(
                        url,
                        params=params,
                        headers=headers
                       # follow_redirects=True
                    )
    
                if response is None:
                       #self.table.rows.clear()
                       return
                if response.status_code == 401:
    
                    await self.toast.show(
                        self.page_ref,
                        "Token inválido",
                        "error"
                    )
    
                    return
    
                if response.status_code != 200:
    
                    await self.toast.show(
                        self.page_ref,
                        f"Error API {response.status_code}",
                        "error"
                    )
    
                    return
    
                self.datos_fijos= response.json()
               
    
            except Exception as ex:
    
                print(ex)
    
                await self.toast.show(
                    self.page_ref,
                    str(ex),
                    "error"
                )

    async def buscar_legajos(self):

        token = settings.TOKEN

        if not token:
            await self.toast.show(
                self.page_ref,
                "Sesión expirada",
                "error"
            )
            return

        headers = {
            "Authorization": f"Bearer {token}"
        }

        url = (
            f"{settings.URL_BACKEND}"
            f"/liquidaciones/legajos-disponibles"
        )

        params = {
            "datos_fijos_id": int(self.cmb_datos_fijos.value)
        }

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    params=params,       # <-- FALTABA ESTO
                    headers=headers,
                    follow_redirects=True
                )

            print("URL:", response.url)
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)

            if response.status_code == 401:

                await self.toast.show(
                    self.page_ref,
                    "Token inválido o expirado",
                    "error"
                )

                return

            if response.status_code != 200:

                await self.toast.show(
                    self.page_ref,
                    f"Error API: {response.status_code}",
                    "error"
                )

                return

            data = response.json()

            self.legajos = [
                {
                    "id": x.get("id"),
                    "cuil": x.get("cuil", ""),
                    "apellido": x.get("apellido", ""),
                    "nombre": x.get("nombre", ""),
                    "sexo": x.get("sexo", ""),
                    "categoria": (
                        x.get("categoria") or {}
                    ).get("nombre", ""),
                    "modalidad_liquidacion": (
                        x.get("modalidad_liquidacion") or {}
                    ).get("nombre", ""),
                    "telefono": x.get("telefono", ""),
                    "activo": x.get("activo", True),
                    "sac": x.get("sac", False),
                    "fecha_ingreso_actual": formatear_fecha(
                        x.get("fecha_ingreso_actual", "")
                    ),
                }
                for x in data
            ]

        except httpx.RequestError as ex:

            print("ERROR CONEXIÓN:", ex)

            await self.toast.show(
                self.page_ref,
                f"Error de conexión: {str(ex)}",
                "error"
            )

        except Exception as ex:

            print("ERROR:", ex)

            await self.toast.show(
                self.page_ref,
                str(ex),
                "error"
            )
        
    async def cambio_datos_fijos(self, e):

            datos_fijo = next(

                (
                    x for x in self.datos_fijos
                    if str(x["id"]) == self.cmb_datos_fijos.value
                ),

                None

            )

            if not datos_fijo:
                return

            self.legajos = {}
            self.modalidad_liquidacion_id = datos_fijo["modalidad_liquidacion_id"]
            await self.cargar_legajos()
      
    async def cambio_legajo(self, e):

            legajo = next(

                (
                    x for x in self.legajos
                    if str(x["id"]) == self.cmb_legajos.value
                ),

                None

            )

            if not legajo:
                return

            self.mostrar_legajo(legajo)

    async def cargar_legajos(self):

            await self.buscar_legajos()
         
            self.cmb_legajos.options = [

                ft.dropdown.Option(
                    key=str(item["id"]),
                    text=f'{item["apellido"]}, {item["nombre"]}'
                )
                for item in self.legajos

            ]

            self.page_ref.update()

    def datos_legajo(self):

        return ft.Container(

            bgcolor="white",

            padding=15,

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            content=ft.Column(

                spacing=0,

                controls=[

                    ft.Text(
                        "Datos del Legajo",
                        size=11,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Row(

                        controls=[

                            ft.Container(

                                expand=True,

                                content=ft.Column(

                                    spacing=6,

                                    controls=[

                                        self.item("Apellido", self.lbl_apellido ),

                                        self.item("Nombre", self.lbl_nombre),

                                        self.item("CUIL", self.lbl_cuil),

                                    ]

                                )

                            ),

                            ft.Container(

                                expand=True,

                                content=ft.Column(

                                    spacing=6,

                                    controls=[

                                        self.item("Categoría", self.lbl_categoria),

                                        self.item("Modalidad", self.lbl_modalidad),

                                        self.item("Empresa", self.lbl_empresa),

                                        self.item(
                                            "Fecha Ingreso actual",
                                            self.lbl_fecha_ingreso_actual
                                        ),

                                    ]

                                )

                            )

                        ]

                    )

                ]

            )

        )

    def mostrar_legajo(self, legajo):
            
            self.lbl_apellido.value = legajo["apellido"]
            self.lbl_nombre.value = legajo["nombre"]
            self.lbl_cuil.value = legajo["cuil"]
            self.lbl_categoria.value = legajo["categoria"]
            self.lbl_modalidad.value = legajo["modalidad_liquidacion"]
           # self.lbl_empresa.value = legajo["empresa"]
            self.lbl_fecha_ingreso_actual.value = legajo["fecha_ingreso_actual"]

            self.page_ref.update()

    def item(self, titulo, control):

        return ft.Row(

            controls=[

                ft.Container(

                    width=130,

                    content=ft.Text(

                        titulo,

                        weight=ft.FontWeight.BOLD,
                        size = 11

                    )

                ),

                control

            ]

        )    
        # =====================================================

    def botonera(self):

        return ft.Container(

            bgcolor="white",

            padding=10,

            border=ft.Border.all(
                1,
                "#E2E8F0"
            ),

            content=ft.Row(

                alignment=ft.MainAxisAlignment.END,

                spacing=10,

                controls=[

                    self.btn_liquidar,

                    self.btn_aceptar,

                    self.btn_cancelar

                ]

            )

        )


        # =====================================================
        # GRILLA
        # =====================================================

    def encabezado_grilla(self):

            return ft.Container(
                
                bgcolor="#E2E8F0",       

                border=ft.Border(
                    bottom=ft.BorderSide(1, "#E2E8F0")
                ),

                padding=8,
              

                content=ft.Row(
                    controls=[
                        ft.Container(
                            expand=1,
                            content=ft.Text(
                                "Código",
                                weight=ft.FontWeight.BOLD,
                                size=12
                            )
                        ),

                        ft.Container(
                            expand=3,
                            content=ft.Text(
                                "Concepto",
                                weight=ft.FontWeight.BOLD,
                                size=12
                            )
                        ),

                        ft.Container(
                            expand=1,
                            content=ft.Text(
                                "Cantidad",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.RIGHT,
                                size=12
                            )
                        ),

                        ft.Container(
                            expand=1,
                            content=ft.Text(
                                "Valor",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.RIGHT,
                                size=12
                            )
                        ),

                        ft.Container(
                            expand=1,
                            content=ft.Text(
                                "Haberes",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.RIGHT,
                                size=12
                                
                            )
                        ),

                        ft.Container(
                            expand=1,
                            content=ft.Text(
                                "Retención",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.RIGHT,
                                size=12
                            )
                        ),

                        ft.Container(
                            expand=1,
                            content=ft.Text(
                                "Total",
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.RIGHT,
                                size=12
                            )
                        ),

                    ]

                )

            )

    def grilla(self):

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
                            #padding=ft.padding.symmetric(horizontal=10, vertical=8),
                            padding=10,

                            content=ft.Text(
                                "Conceptos Liquidados",
                                size=16,
                                weight=ft.FontWeight.BOLD
                            )

                        ),

                       ft.Container(
                            margin=ft.Margin.only(left=8, right=8),
                            content=self.encabezado_grilla(),
                        ),

                        ft.Container(
                            margin=ft.Margin.only(left=8, right=8),
                            content=self.lista_conceptos,
                        ),

                        #self.lista_conceptos

                    ]

                )

            )
    def agregar_fila(self, item):

        cantidad = float(item["cantidad"])
        valor = float(item["valor"])
        haber = float(item["haber"])
        retencion = float(item["retencion"])
        total = float(item["total"])

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

                    ft.Text(
                        item["codigo"],
                        expand=1,
                        size=11
                    ),

                    ft.Text(
                        item["concepto"],
                        expand=3,
                        size=11
                    ),

                    ft.Text(
                        f"{cantidad:.2f}",
                        expand=1,
                        text_align=ft.TextAlign.RIGHT,
                        size=11
                    ),

                    ft.Text(
                        f"{valor:,.2f}",
                        expand=1,
                        text_align=ft.TextAlign.RIGHT,
                        size=11
                    ),

                    ft.Text(
                        f"{haber:,.2f}",
                        expand=1,
                        text_align=ft.TextAlign.RIGHT,
                        size=11
                    ),

                    ft.Text(
                        f"{retencion:,.2f}",
                        expand=1,
                        text_align=ft.TextAlign.RIGHT,
                        size=11
                    ),

                    ft.Text(
                        f"{total:,.2f}",
                        expand=1,
                        text_align=ft.TextAlign.RIGHT,
                        size=11
                    )

                ]
            )
        )

        self.lista_conceptos.controls.append(fila)
           
    """   def build(self):

        return ft.Container(

            expand=True,

            bgcolor="#F8FAFC",

            padding=10,

            content=ft.Column(

                expand=True,

                spacing=10,

                controls=[

                    ft.Row(

                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Column(

                                spacing=2,

                                controls=[

                                    ft.Text(
                                        "Liquidación de haberes",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color="#0F172A",
                                    ),

                                    ft.Text(
                                        "Nueva liquidación",
                                        size=11,
                                        color="#64748B",
                                    ),

                                ],
                            ),

                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                on_click=lambda e: self.page_ref.layout.change_view(
                                    "liquidacion_haberes"
                                ),
                            ),

                        ],
                    ),

                    ft.Divider(height=1),

                    self.encabezado(),

                    ft.Container(
                        expand=True,
                        content=self.cuerpo(),
                    ),

                ],

            ),

        )
    """
    def build(self):

            return ft.Stack(

                expand=True,

                controls=[

                    ft.Container(

                        expand=True,

                        bgcolor="#F8FAFC",

                        padding=10,

                        content=ft.Column(

                            expand=True,

                            spacing=10,

                            controls=[

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[

                                        ft.Column(
                                            spacing=2,
                                            controls=[
                                                ft.Text(
                                                    "Liquidación de haberes",
                                                    size=16,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(
                                                    "Nueva liquidación",
                                                    size=11,
                                                    color="#64748B",
                                                ),
                                            ],
                                        ),

                                        ft.IconButton(
                                            icon=ft.Icons.CLOSE,
                                            on_click=lambda e:
                                                self.page_ref.layout.change_view(
                                                    "liquidacion_haberes"
                                                ),
                                        ),

                                    ],
                                ),

                                ft.Divider(height=1),

                                self.encabezado(),

                                ft.Container(
                                    expand=True,
                                    content=self.cuerpo(),
                                ),

                            ],

                        ),

                    ),

                    self.loading,
                    self.toast,   

                ],

            )

    def cuerpo(self):

            return ft.Column(

                expand=True,
                
                scroll=ft.ScrollMode.AUTO,

                spacing=10,

                controls=[


                    self.datos_legajo(),

                    self.botonera(),

                    self.grilla(),

                    self.totales()

                ]

            )
   
    async def set_mode(self, id):
          
            self.id = id
    
            if id == 0:
                pass
                #self.nuevo()
    
            else:
                self.lbl_titulo.value = "Editar Liquidación"
               # await self.cargar(id)
            
            self.limpiar_controles()
            self.cmb_datos_fijos.options.clear()
            self.datos_fijos = []
    
    '''async def liquidar(self, e):

        if  not self.cmb_legajos.value :
            print("alert")
            await self.toast.show(
                self.page_ref,
                    "Debe seleccionar un legajo.",
                    "alert"
            )   
            return


        self.loading.visible = True

        self.page_ref.update()

   
        try:

            self.lista_conceptos.controls.clear()

            resultado = await self.api_liquidar()

            if not resultado:
                return

            total_haberes = 0
            total_retenciones = 0

            for item in resultado["detalle"]:

                self.agregar_fila(item)

                total_haberes += item["haber"]
                total_retenciones += item["retencion"]

            self.lbl_total_haberes.value = f"${total_haberes:,.2f}"
            self.lbl_total_retenciones.value = f"${total_retenciones:,.2f}"
            self.lbl_neto.value = f"${resultado['neto']:,.2f}"


        finally:
            await asyncio.sleep(1)

            self.loading.visible = False

            self.page_ref.update()'''

 
    async def liquidar(self, e):

        # =====================================================
        # VALIDAR LEGAJO
        # =====================================================

        if not self.cmb_legajos.value:

            await self.toast.show(
                self.page_ref,
                "Debe seleccionar un legajo.",
                "alert"
            )

            return

        # =====================================================
        # MOSTRAR LOADING
        # =====================================================

        self.loading.visible = True
        self.page_ref.update()

        try:

            # =================================================
            # LIMPIAR LIQUIDACIÓN ANTERIOR
            # =================================================

            self.lista_conceptos.controls.clear()

            self.lbl_total_haberes.value = "$ 0,00"
            self.lbl_total_retenciones.value = "$ 0,00"
            self.lbl_neto.value = "$ 0,00"

            # =================================================
            # EJECUTAR LIQUIDACIÓN
            # =================================================

            resultado = await self.api_liquidar()

            if not resultado:
                return

            # =================================================
            # GUARDAR RESULTADO
            # Lo vamos a necesitar cuando presionemos Aceptar
            # =================================================

            self.resultado_liquidacion = resultado

            # =================================================
            # TOTALES
            # =================================================

            total_haberes = Decimal("0")
            total_retenciones = Decimal("0")

            # =================================================
            # DETALLE
            # =================================================

            for item in resultado.get("detalle", []):

                self.agregar_fila(item)

                total_haberes += Decimal(
                    str(item.get("haber", "0"))
                )

                total_retenciones += Decimal(
                    str(item.get("retencion", "0"))
                )

            # =================================================
            # MOSTRAR TOTALES
            # =================================================

            self.lbl_total_haberes.value = (
                f"${total_haberes:,.2f}"
            )

            self.lbl_total_retenciones.value = (
                f"${total_retenciones:,.2f}"
            )

            neto = Decimal(
                str(resultado.get("neto", "0"))
            )

            self.lbl_neto.value = (
                f"${neto:,.2f}"
            )

            self.page_ref.update()

        except Exception as ex:

            print("ERROR AL LIQUIDAR:", ex)

            await self.toast.show(
                self.page_ref,
                f"Error al liquidar: {str(ex)}",
                "error"
            )

        finally:

            await asyncio.sleep(0.5)

            self.loading.visible = False

            self.page_ref.update()

    async def aceptar(self, e):

        if len(self.lista_conceptos.controls) == 0:
            await self.toast.show(
                 self.page_ref,
                            "No hay liquidacion.",
                            "alert"
                        )
            
            return
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar aceptacion"),
            content=ft.Text("¿Realmente desea guardar esta liquidacion?"),
                    actions_alignment=ft.MainAxisAlignment.END,
                    actions=[
            
                        ft.OutlinedButton(
                            "Cancelar",
                            on_click=lambda e: cerrar()
                        ),
            
                        ft.FilledButton(
                                "Aceptar",
                                bgcolor="#111111",
                                color="white",
                                on_click=lambda e: confirmar()
                            )
                        ]
            )
            
        def cerrar():
            
            dialog.open = False
            
            self.page_ref.update()
            
        async def ejecutar():
            
            dialog.open = False
            
            self.page_ref.update()

            await self.registrar_liquidacion()
            await self.cargar_legajos()
            
        def confirmar():
            
                self.page_ref.run_task(
                    ejecutar
                )
            
        if dialog not in self.page_ref.overlay:
                        self.page_ref.overlay.append(dialog)
            
        self.page_ref.dialog = dialog
            
        dialog.open = True
            
        self.page_ref.update()

    async def registrar_liquidacion(self):

        token = settings.TOKEN

        if not token:
            await self.toast.show(
                self.page_ref,
                "Sesión expirada",
                "error"
            )
            return

        # =====================================================
        # Validar datos seleccionados
        # =====================================================

        if not self.cmb_datos_fijos.value:
            await self.toast.show(
                self.page_ref,
                "Debe seleccionar los datos fijos.",
                "alert"
            )
            return

        if not self.cmb_legajos.value:
            await self.toast.show(
                self.page_ref,
                "Debe seleccionar un legajo.",
                "alert"
            )
            return

        if not self.resultado_liquidacion:
            await self.toast.show(
                self.page_ref,
                "Debe liquidar antes de guardar.",
                "alert"
            )
            return

        # =====================================================
        # Buscar datos fijos seleccionados
        # =====================================================

        datos_fijo = next(
            (
                x for x in self.datos_fijos
                if str(x["id"]) == str(self.cmb_datos_fijos.value)
            ),
            None
        )

        if not datos_fijo:
            await self.toast.show(
                self.page_ref,
                "No se encontraron los datos fijos seleccionados.",
                "error"
            )
            return

        # =====================================================
        # Construir líneas
        # =====================================================

        lineas = []

        for item in self.resultado_liquidacion["detalle"]:

            lineas.append({
                "concepto_id": item["concepto_id"],
                "concepto": item["concepto"],
                "cantidad": item["cantidad"],
                "valor": item["valor"],
                "haber": item["haber"],
                "retencion": item["retencion"],
                "total": item["total"]
            })

        # =====================================================
        # Payload
        # =====================================================

        payload = {
            "legajo_id": int(self.cmb_legajos.value),

            "datos_fijos_liquidacion_id": int(
                self.cmb_datos_fijos.value
            ),

            "tipo_liquidacion_id": int(
                datos_fijo["tipo_liquidacion_id"]
            ),

            "lineas": lineas
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        url = f"{settings.URL_BACKEND}/liquidaciones"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(
                    url,
                    json=payload,
                    headers=headers
                )

            # =================================================
            # Liquidación creada
            # =================================================

            if response.status_code == 200:

                await self.toast.show(
                    self.page_ref,
                    "Liquidación registrada.",
                    "success"
                )

                self.limpiar_controles()

                self.resultado_liquidacion = None

                self.page_ref.update()

            # =================================================
            # Token
            # =================================================

            elif response.status_code == 401:

                await self.toast.show(
                    self.page_ref,
                    "Token inválido o expirado.",
                    "error"
                )

            # =================================================
            # Error API
            # =================================================

            else:
            
                try:
                    detalle = response.json().get(
                        "detail",
                        "No se pudo registrar la liquidación."
                    )
                except Exception:
                    detalle = response.text
                  

                await self.toast.show(
                    self.page_ref,
                    detalle,
                    "error"
                )

        except httpx.RequestError as ex:
            print(str(ex))
            await self.toast.show(
                self.page_ref,
                f"Error de conexión: {str(ex)}",
                "error"
            )    
        
    async  def cancelar(self, e):

        if len(self.lista_conceptos.controls) == 0:              
            return
               
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar cancelacion"),
            content=ft.Text("¿Realmente desea cancelar esta liquidacion?"),
                    actions_alignment=ft.MainAxisAlignment.END,
                    actions=[
                   
                        ft.OutlinedButton(
                             "Cancelar",
                              on_click=lambda e: cerrar()
                        ),
                   
                        ft.FilledButton(
                            "Aceptar",
                            bgcolor="#111111",
                            color="white",
                            on_click=lambda e: confirmar()
                        )
                    ]
        )
                   
        def cerrar():
                   
            dialog.open = False
                   
            self.page_ref.update()


            
                   
        async def ejecutar():
                
            dialog.open = False
                   
            self.page_ref.update()
       
            await self.ejecutar_cancelacion()
                   
        def confirmar():
                   
            self.page_ref.run_task(
                           ejecutar
            )
                   
        if dialog not in self.page_ref.overlay:
            self.page_ref.overlay.append(dialog)
                   
        self.page_ref.dialog = dialog
                   
        dialog.open = True
                   
        self.page_ref.update()
       
    async def ejecutar_cancelacion(self):

        self.cmb_datos_fijos.value = None 
        
        # ==========================
        # Limpiar selección Legajo
        # ==========================

        self.cmb_legajos.value = None

        self.cmb_legajos.options.clear()


        # ==========================
        # Limpiar variables internas
        # ==========================


        self.modalidad_liquidacion_id = 0

        self.legajos = []


        # ==========================
        # Limpiar datos del legajo
        # ==========================

        self.lbl_apellido.value = "-"
        self.lbl_nombre.value = "-"
        self.lbl_cuil.value = "-"
        self.lbl_categoria.value = "-"
        self.lbl_modalidad.value = "-"
        self.lbl_empresa.value = "-"
        self.lbl_fecha_ingreso_actual.value = "-"


        # ==========================
        # Limpiar conceptos liquidados
        # ==========================

        self.lista_conceptos.controls.clear()


        # ==========================
        # Limpiar totales
        # ==========================

        self.lbl_total_haberes.value = "$ 0,00"

        self.lbl_total_retenciones.value = "$ 0,00"

        self.lbl_neto.value = "$ 0,00"

        self.page_ref.update()


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

                        horizontal_alignment=ft.CrossAxisAlignment.START,

                        spacing=5,

                        controls=[

                            ft.Row(

                                width=340,

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Total Haberes:",
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                    self.lbl_total_haberes,

                                ]

                            ),

                            ft.Row(

                                width=340,

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Total Retenciones:",
                                        weight=ft.FontWeight.BOLD,
                                    ),

                                    self.lbl_total_retenciones,

                                ]

                            ),

                            ft.Divider(height=5),

                            ft.Row(

                                width=340,

                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls=[

                                    ft.Text(
                                        "Neto a Cobrar:",
                                        weight=ft.FontWeight.BOLD,
                                        size=16,
                                    ),

                                    self.lbl_neto,

                                ]

                            ),

                        ]

                    )

                ]

            )

        ) 
    
    async def api_liquidar(self):
        
        token = settings.TOKEN
          
        if not token:
            await self.toast.show(
                self.page_ref,
                    "Sesión expirada",
                       "error"
            )
          
            return
          
         

        payload = {
                "datos_fijos_id": self.cmb_datos_fijos.value ,
                "legajo_id": self.cmb_legajos.value            }

        headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        url = f"{settings.URL_BACKEND}/liquidaciones/liquidar"  
        async with httpx.AsyncClient() as client:

                response = await client.post(
                    url,
                    json=payload,
                    headers=headers
                )

                if response.status_code == 200:

                    resultado = response.json()

                    return resultado

                else:

                    print(
                        "Error:",
                        response.status_code,
                        response.text
                    )

                    return None