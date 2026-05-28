import asyncio

import flet as ft
import httpx
from  core.config import settings

class ModalLegajo:

    def __init__(self, page, on_success=None):
  
        self.on_success = on_success
        self.page = page
        self.legajo_id = None
        # =========================
        # LOADER
        # =========================
        self.loading = ft.ProgressRing(visible=False)

        COMMON_HEIGHT = 55

        # =========================
        # CAMPOS
        # =========================
        self.txt_cuil = ft.TextField(
            label="CUIL",
            width=350,
            height=70,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=11,
            on_change=self.solo_numeros,
        )

        self.txt_apellido = ft.TextField(
            label="Apellido",
            expand=True,
            height=COMMON_HEIGHT,
            on_change=self.force_upper
        )

        self.txt_nombre = ft.TextField(
            label="Nombre",
            expand=True,
            height=COMMON_HEIGHT,
            on_change=self.force_upper
        )

        self.ddl_sexo = ft.Dropdown(
            label="Sexo",
            expand=True,
            height=COMMON_HEIGHT,
            options=[
                ft.dropdown.Option("M"),
                ft.dropdown.Option("F"),
            ],
        )

        self.ddl_categoria = ft.Dropdown(
                label="Categoría",
                expand=True,
                height=COMMON_HEIGHT,
                options=[],
)

        self.ddl_modalidad = ft.Dropdown(
                label="Modalidad",
                expand=True,
                height=COMMON_HEIGHT,
                options=[],
            )

        self.txt_telefono = ft.TextField(
            label="Teléfono",
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=15,
            on_change=self.solo_numeros,
        )

        self.chk_sac = ft.Checkbox(label="SAC", value=False)
        self.chk_activo = ft.Checkbox(label="Activo", value=True)

        self.lbl_mensaje = ft.Text( "",
            size=14,
            color=ft.Colors.RED_400,
            visible=False,
        )

        # =========================
        # DIALOG
        # =========================
        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor="white",
            shape=ft.RoundedRectangleBorder(radius=0),
            content_padding=0,
            inset_padding=20,
            content=ft.Container(
                width=750,
                padding=20,
                content=ft.Column(
                    tight=True,
                    spacing=15,
                    controls=[

                        # HEADER
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=2,
                                    controls=[
                                        ft.Text(
                                            "Nuevo Legajo",
                                            size=18,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            "Complete los datos del empleado",
                                            size=11,
                                            color="#64748B",
                                        ),
                                        self.lbl_mensaje
                                    ],
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    on_click=self.cerrar
                                ),
                            ],
                        ),

                        ft.Divider(),

                        # FORM
                        ft.Column(
                            spacing=12,
                            controls=[

                                ft.Row([self.txt_cuil]),

                                ft.Row([
                                    self.txt_apellido,
                                    self.txt_nombre
                                ]),

                                ft.Row([
                                    self.ddl_sexo,
                                    self.ddl_categoria
                                ]),

                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        self.ddl_modalidad,
                                        self.txt_telefono,
                                    ],
                                ),

                                ft.Row([
                                    self.chk_sac,
                                    self.chk_activo
                                ]),
                            ],
                        ),

                        ft.Divider(),

                        # FOOTER
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                self.loading,

                                ft.OutlinedButton(
                                    "Cancelar",
                                    on_click=self.cerrar
                                ),

                                ft.FilledButton(
                                    "Guardar",
                                    on_click=self.guardar
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )

        self.page.overlay.append(self.dialog)

    # =========================
    # ABRIR
    # =========================
    async def abrir_nuevo(self, e):
        self.legajo_id=0
        self.limpiar()
        await self.cargar_categoria()
        await self.cargar_modalidad()

        self.dialog.open = True

        self.page.update()

    # =========================
    # EDIATR
    # =========================
    async def editar(self, e, item):
        
        self.limpiar()

        self.modo_edicion = True
        self.legajo_id = item["id"]

        await self.cargar_categoria()
        await self.cargar_modalidad()

        # =========================
        # CARGAR DATOS
        # =========================
        self.txt_cuil.value = item["cuil"]
        self.txt_apellido.value = item["apellido"]
        self.txt_nombre.value = item["nombre"]
        self.ddl_sexo.value = item["sexo"]

        self.ddl_categoria.value = str(item["categoria_id"])
        self.ddl_modalidad.value = str(item["modalidad_liquidacion_id"])

        self.txt_telefono.value = item["telefono"]

        self.chk_sac.value = item["sac"]
        self.chk_activo.value = item["activo"]

        self.dialog.open = True

        self.page.update()

     
    # =========================
    # CERRAR
    # =========================
    async def cerrar(self, e):

        self.dialog.open = False

        self.page.update()

    # =========================
    # LIMPIAR
    # =========================
    def limpiar(self):
        self.lbl_mensaje.visible= False
        self.lbl_mensaje.value =  ""
        self.txt_cuil.value = ""
        self.txt_apellido.value = ""
        self.txt_nombre.value = ""
        self.txt_telefono.value = ""

        self.txt_cuil.error = None
        self.txt_apellido.error = None
        self.txt_nombre.error = None
        self.txt_telefono.error = None

        self.ddl_sexo.value = None
        self.ddl_categoria.value = None
        self.ddl_modalidad.value = None

        self.ddl_sexo.error_text = None
        self.ddl_categoria.error_text = None
        self.ddl_modalidad.error_text = None

        self.chk_sac.value = False
        self.chk_activo.value = True

        self.page.update()

    # =========================
    # VALIDAR
    # =========================
    async def validar_formulario(self):

        valido = True

        if not self.txt_cuil.value:
            self.txt_cuil.error = "El CUIL es obligatorio"
            valido = False

        if not self.txt_apellido.value:
            self.txt_apellido.error = "Apellido obligatorio"
            valido = False

        if not self.txt_nombre.value:
            self.txt_nombre.error = "Nombre obligatorio"
            valido = False

        if not self.ddl_sexo.value:
            self.ddl_sexo.error_text = "Seleccione sexo"
            valido = False

        if not self.ddl_categoria.value:
            self.ddl_categoria.error_text = "Seleccione categoría"
            valido = False

        if not self.ddl_modalidad.value:
            self.ddl_modalidad.error_text = "Seleccione modalidad"
            valido = False

        self.page.update()

        return valido

    # =========================
    # GUARDAR
    # =========================
    async def guardar(self, e):

        if not await self.validar_formulario():
            return

        self.loading.visible = True

        self.page.update()

        try:

            data = {
                "cuil": self.txt_cuil.value,
                "apellido": self.txt_apellido.value,
                "nombre": self.txt_nombre.value,
                "sexo": self.ddl_sexo.value,
                "categoria_id": self.ddl_categoria.value,
                "modalidad_liquidacion_id": self.ddl_modalidad.value,
                "sac": self.chk_sac.value,
                "activo": self.chk_activo.value,
                "telefono": self.txt_telefono.value
            }
            if self.legajo_id == 0:
                ok = await self.api_crear(data)
            else:
                ok = await self.api_editar(data)
          

            if ok:
                self.dialog.open = False
                self.page.update()
               
                if self.on_success:
                    await   self.on_success()

                

        finally:

            self.loading.visible = False

            self.page.update()

    # =========================
    # SOLO NUMEROS
    # =========================
    def solo_numeros(self, e):

        limpio = "".join(
            filter(str.isdigit, e.control.value or "")
        )

        if e.control.value != limpio:

            e.control.value = limpio

            e.control.update()

    # =========================
    # API
    # =========================
    async def api_crear(self, data):
    
        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/legajos"

        try:

            async with httpx.AsyncClient() as client:

                response = await client.post(
                    url,
                    json=data,
                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )

            # SUCCESS
            if response.status_code in (200, 201):
                self.lbl_mensaje.value = "Se guardo con exito el legajo."
                self.lbl_mensaje.color =  "#069206"
                self.lbl_mensaje.visible = True
                self.page.update()
                await asyncio.sleep(3)    
                return True

            # ERROR API
            data = response.json()
            msg = data.get("detail", "Error desconocido")
            self.lbl_mensaje.value = msg#[0]["msg"]
            self.lbl_mensaje.color = "#DC2626"
            self.lbl_mensaje.visible = True
            self.page.update()
          
            return False

        except Exception as ex:
            print(ex.args[0])
            self.lbl_mensaje.value = ex
            self.lbl_mensaje.color= "#DC2626"
            self.lbl_mensaje.visible = True
            self.page.update() 
           
            return False
    async def api_editar(self, data):

        token = settings.TOKEN

        url = f"{settings.URL_BACKEND}/legajos/{self.legajo_id}"

        async with httpx.AsyncClient() as client:

            response = await client.put(
                url,
                json=data,
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        return response.status_code in (200, 201)
    
    async def cargar_categoria(self):

        token = settings.TOKEN

        headers = {
            "Authorization": f"Bearer {token}"
        }

        async with httpx.AsyncClient() as client:

        # CATEGORIAS
            response_categoria = await client.get(
                f"{settings.URL_BACKEND}/categorias",
                headers=headers
            )
      
        if response_categoria.status_code == 200:

            categorias = response_categoria.json()
           
            self.ddl_categoria.options = [
                ft.dropdown.Option(
                    key=str(item["id"]),
                    text=item["nombre"]
                )
                for item in categorias
            ]           

        self.page.update()
    async def cargar_modalidad(self):

        token = settings.TOKEN

        headers = {
            "Authorization": f"Bearer {token}"
        }

        async with httpx.AsyncClient() as client:
        # MODALIDADES
            response_modalidad = await client.get(
                f"{settings.URL_BACKEND}/modalidades",
                headers=headers
            )

            if response_modalidad.status_code == 200:

                modalidades = response_modalidad.json()

                self.ddl_modalidad.options = [
                    ft.dropdown.Option(
                        key=str(item["id"]),
                        text=item["nombre"]
                    )
                    for item in modalidades
                ]

            self.page.update()
    def force_upper(self, e):
        e.control.value = (e.control.value or "").upper()
        e.control.update()        