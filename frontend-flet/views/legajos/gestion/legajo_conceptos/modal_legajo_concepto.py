import asyncio

import flet as ft
import httpx

from core.config import settings
from components.alerts import Toast
from components.datapicker import DatePickerCustom

class ModalLegajoConcepto(ft.AlertDialog):

    def __init__(self, page, on_success=None):
        super().__init__(modal=True)

        self.page_ref = page
        self.on_success = on_success

        self.legajo_id = 0
        self.item_id = 0
        self.modalidad_pago_id = 0

        self.toast = Toast()
        self.shape = ft.RoundedRectangleBorder(radius=0)
        # =========================
        # TITLE
        # =========================
        self.titulo_accion = "Agregar Nuevo Concepto al Legajo"
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
        )

        self.bgcolor = "white"
        self.content_padding = 0
        self.inset_padding = 20

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
        # FIELDS
        # =========================
        self.cmb_concepto = ft.Dropdown(label="Concepto", options=[], expand=True)
        ft.Margin(4, 0, 0, 0),
        #self.dp_desde = DatePickerCustom(
        #    self.page_ref,
        #    label="Fecha Desde"
        #)
        #self.dp_hasta = DatePickerCustom(
        #    self.page_ref,
        #    label="Fecha Hasta"
        #)
        self.txt_valor = ft.TextField(label="Valor", 
                                      expand=True,   
                                      value="0.00",
                                      max_length=10,
                                      keyboard_type=ft.KeyboardType.NUMBER,
                                      on_change=self.solo_decimal)
      
        self.chk_activo = ft.Checkbox(label="Activo", value=True)

        self.loading = ft.ProgressRing(visible=False)

        # =========================
        # CONTENT (COMPACTO)
        # =========================
        self.content = ft.Container(
    width=700,
    padding=15,
    content=ft.Column(
        spacing=10,
        tight=True,
        controls=[

            # CONCEPTO + VALOR
            ft.Row(
                spacing=10,
                controls=[
                    ft.Container(
                        expand=2,
                        margin=ft.Margin(0, -14, 0, 0),
                        content=self.cmb_concepto
                    ),

                    ft.Container(
                        expand=1,
                        content=self.txt_valor
                    ),
                ]
            ),

            # ACTIVO
            ft.Container(
                alignment=ft.Alignment.CENTER,
                content=self.chk_activo
            ),

            # DIVIDER
            ft.Divider(height=1),

            # FOOTER
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[

                    self.loading,

                    ft.OutlinedButton(
                        "Cancelar",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(
                                radius=0
                            ),
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
                            shape=ft.RoundedRectangleBorder(
                                radius=0
                            ),
                            padding=12
                        ),
                        on_click=self.guardar
                    ),
                ]
            )
        ]
    )
)

    async def abrir(self, legajo_id, item=None):

        self.limpiar()

        self.legajo_id = legajo_id

        legajo = await self.obtener_legajo_by_id(legajo_id)
        self.modalidad_pago_id= legajo.get('modalidad_pago_id')
       
        await self.cargar_conceptos()
       

        if item:
            self.titulo_accion = "Editar Concepto del Legajo"
            self.lbl_titulo_accion.value = self.titulo_accion
            self.item_id = item["id"]
            self.cmb_concepto.value = item["concepto_id"]
            #self.dp_desde.value = item["fecha_desde"]
            #self.dp_hasta.value = item["fecha_hasta"] or ""
            self.txt_valor.value = str(item["valor"])
            self.chk_activo.value = item["activo"]

        if self not in self.page_ref.overlay:
            self.page_ref.overlay.append(self)

        self.page_ref.dialog = self
        self.open = True
        self.page_ref.update()

    async def cargar_conceptos(self):
 
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{settings.URL_BACKEND}/conceptos/modalidad-pago/{self.modalidad_pago_id}",
                headers={
                    "Authorization": f"Bearer {settings.TOKEN}"
                }
            )

        self.cmb_concepto.options = [
            ft.dropdown.Option(str(x["id"]), x["nombre"])
            for x in r.json()
        ]
  
    def limpiar(self):
        self.item_id = 0
        self.cmb_concepto.value = None
        self.cmb_concepto.value = ""
        self.txt_valor.error = None
        #self.dp_desde.value = ""
        #self.dp_hasta.value = ""
        self.txt_valor.value = "0.00"
        self.chk_activo.value = True
        self.lbl_mensaje.value = ""

    async def guardar(self, e):

        valido = await self.validar_formulario()

        if not valido:
            return

        self.loading.visible = True
        self.page_ref.update()
        try :

            data = {
                #"legajo_id": self.legajo_id,
                "concepto_id": int(self.cmb_concepto.value),
                #"fecha_desde": self.dp_desde.value,
                #"fecha_hasta": self.dp_hasta.value or None,
                "valor": float(self.txt_valor.value or 0),
                "activo": self.chk_activo.value
            }

            ok = await self.api_crear(data)

            if not ok:
                raise Exception()
                #return
           
            self.lbl_mensaje.value = (
                    "Registrado creado correctamente"
                )

            self.lbl_mensaje.color = "#15803D"
            self.lbl_mensaje.visible = True
            self.page.update()
            await asyncio.sleep(1)
             
            self.open = False
            self.page_ref.dialog = None
            self.page_ref.update()
           
            if self.on_success:
                await self.on_success()

        except Exception as  ex:
            self.lbl_mensaje.value = "Ocurrio un Error al intentar guardar"
            self.lbl_mensaje.color = "#FA0909"
            self.lbl_mensaje.visible = True
            await asyncio.sleep(1)
        finally:
            self.loading.visible = False
            self.page_ref.update()

    def cerrar(self, e=None):
        self.open = False
        self.page_ref.dialog = None
        self.page_ref.update()
    
    def solo_decimal(self, e):
        valor = e.control.value

        permitido = ""

        separador = False

        for c in valor:

            if c.isdigit():
                permitido += c

            elif c in [".", ","] and not separador:
                permitido += "."
                separador = True

        e.control.value = permitido

        e.control.update()

    async def obtener_legajo_by_id(self,legajo_id:int):
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
            return

        data = response.json()
        legajo = {
                    "id" : data.get('id'),
                    "cuil": data.get("cuil", 0),
                    "fecha_ingreso_actual" :  data.get("fecha_ingreso_actual", ""),
                    "apellido": data.get("apellido", ""),
                    "nombre": data.get("nombre", ""),
                    "sexo": data.get("sexo",""),
                    "categoria_id": data.get("categoria_id"),
                    "modalidad_liquidacion_id":  data.get("modalidad_liquidacion_id"),
                    "telefono": data.get("telefono", ""),
                    "activo": data.get("activo", True),
                    "sac":  data.get("sac", False),
                    "modalidad_pago_id" : data.get("modalidad_pago_id"),
                    "valor_modalidad_pago" : data.get("valor_modalidad_pago")
                }
        
        return legajo
    
    async def validar_formulario(self):

        # limpiar errores anteriores
        self.cmb_concepto.error_text = None
        self.txt_valor.error = None

        # validar concepto
        if not self.cmb_concepto.value:
            self.cmb_concepto.error_text = (
                "Debe seleccionar un concepto."
            )

            self.page_ref.update()

            return False

        # validar valor vacío
        valor = (self.txt_valor.value or "").strip()
       
        if valor == "":

            self.txt_valor.error= (
                "Debe ingresar un valor."
            )

            self.page_ref.update()

            return False

        # validar número
        try:

            numero = float(valor)

            if numero < 0:

                self.txt_valor.error = (
                    "El valor no puede ser negativo."
                )

                self.page_ref.update()

                return False

        except ValueError:

            self.txt_valor.error_text = (
                "Valor inválido."
            )

            self.page_ref.update()

            return False

        self.page_ref.update()

        return True
    
    async def api_crear(self, data):
        token = settings.TOKEN

        url = (
            f"{settings.URL_BACKEND}/legajos/{self.legajo_id}/conceptos"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(

                    url,

                    json=data,

                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )


            if response.status_code in (200, 201):

                return True

            data = response.json()

            '''self.lbl_mensaje.value = data.get(
                "detail",
                "Error desconocido"
            )

            self.lbl_mensaje.color = "#DC2626"

            self.lbl_mensaje.visible = True

            self.page.update()'''

            return False

        except Exception as ex:

            print(ex)

            self.lbl_mensaje.value = "Ocurrio un Error al intentar guardar"

            self.lbl_mensaje.color = "#DC2626"

            self.lbl_mensaje.visible = True

            self.page.update()

            return False
    
    async def api_editar(self, data):

        token = settings.TOKEN

        url = (
             f"{settings.URL_BACKEND}/legajo-conceptos/{self.item_id}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.pur(

                    url,

                    json=data,

                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )


            if response.status_code in (200, 201):

                return True

            data = response.json()

            self.lbl_mensaje.value = data.get(
                "detail",
                "Error desconocido"
            )

            self.lbl_mensaje.color = "#DC2626"

            self.lbl_mensaje.visible = True

            self.page.update()

            return False

        except Exception as ex:

            print(ex)

            self.lbl_mensaje.value = "Ocurrio un Error al intentar guardar"

            self.lbl_mensaje.color = "#DC2626"

            self.lbl_mensaje.visible = True

            self.page.update()

            return False