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
        self.title = self.lbl_titulo_accion

        self.bgcolor = "white"
        self.content_padding = 0
        self.inset_padding = 20

        # =========================
        # FIELDS
        # =========================
        self.cmb_concepto = ft.Dropdown(label="Concepto", options=[], expand=True)
        ft.Margin(4, 0, 0, 0),
        self.dp_desde = DatePickerCustom(
            self.page_ref,
            label="Fecha Desde"
        )
        self.dp_hasta = DatePickerCustom(
            self.page_ref,
            label="Fecha Hasta"
        )
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
                spacing=6,
                tight=True,
                controls=[

                    # CONCEPTO (pegado arriba)
                    ft.Container(
                        margin=ft.Margin(0, 0, 0, 2),
                        content=self.cmb_concepto
                    ),

                    # DESDE / HASTA / VALOR
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Container(expand=1, content=self.dp_desde),
                            ft.Container(expand=1, content=self.dp_hasta),
                            ft.Container(expand=1, content=self.txt_valor,),
                        ]
                    ),

                    # ACTIVO (cerca del bloque anterior)
                    ft.Container(
                        margin=ft.Margin(0, 2, 0, 0),
                        content=self.chk_activo
                    ),

                    # DIVIDER compacto
                    ft.Container(
                        margin=ft.Margin(0, 6, 0, 6),
                        content=ft.Divider(height=1)
                    ),

                    # FOOTER
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[

                            self.loading,

                            ft.OutlinedButton(
                                "Cancelar",
                             
                                style=ft.ButtonStyle(   
                                    shape=ft.RoundedRectangleBorder(radius=0),
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
                                    shape=ft.RoundedRectangleBorder(radius=0),
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
            self.dp_desde.value = item["fecha_desde"]
            self.dp_hasta.value = item["fecha_hasta"] or ""
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
                f"{settings.URL_BACKEND}/conceptos",
                params={
                    "modalidad_pago_id": self.modalidad_pago_id
                },
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
        self.cmb_concepto.value = ""
        self.dp_desde.value = ""
        self.dp_hasta.value = ""
        self.txt_valor.value = "0.00"
        self.chk_activo.value = True

    async def guardar(self, e):

        valido = await self.validar_formulario()

        if not valido:
            return


        self.loading.visible = True
        self.page_ref.update()

        data = {
            "legajo_id": self.legajo_id,
            "concepto_id": int(self.cmb_concepto.value),
            "fecha_desde": self.dp_desde.value,
            "fecha_hasta": self.dp_hasta.value or None,
            "valor": float(self.txt_valor.value or 0),
            "activo": self.chk_activo.value
        }

        async with httpx.AsyncClient() as client:

            if self.item_id:
                await client.put(
                    f"{settings.URL_BACKEND}/legajo-conceptos/{self.item_id}",
                    json=data
                )
            else:
                await client.post(
                    f"{settings.URL_BACKEND}/legajo-conceptos",
                    json=data
                )

        self.loading.visible = False
        self.open = False
        self.page_ref.dialog = None
        self.page_ref.update()

        if self.on_success:
            await self.on_success()

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

        if not self.cmb_concepto.value:
            await self.toast.show(
                self.page_ref,
                "Debe seleccionar un concepto",
                "error"
            )
            return False

        if not self.dp_desde.value:
            await self.toast.show(
                self.page_ref,
                "Debe ingresar Fecha Desde",
                "warning"
            )
            return False

        if self.txt_valor.value in ["", ".", None]:
            await self.toast.show(
                self.page_ref,
                "Debe ingresar un valor válido",
                "warning"
            )
            return False

        try:

            valor = float(self.txt_valor.value)

            if valor < 0:
                await self.toast.show(
                    self.page_ref,
                    "El valor no puede ser negativo",
                    "warning"
                )
                return False

        except Exception:

            await self.toast.show(
                self.page_ref,
                "Valor inválido",
                "warning"
            )
            return False

        if (
            self.dp_hasta.value
            and self.dp_desde.value
            and self.dp_hasta.value < self.dp_desde.value
        ):

            await self.toast.show(
                self.page_ref,
                "Fecha Hasta no puede ser menor que Fecha Desde",
                "warning"
            )

            return False

        return True
    