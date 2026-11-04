# AGENTS.md — Frontend SIGES

Instrucciones para que la IA trabaje en el frontend de SIGES respetando la arquitectura y convenciones existentes.

## Qué es este proyecto

- Aplicación de escritorio en **Python** con **Flet 0.85.3** (`ft.run(main)`), no es una SPA web.
- El código vive en `frontend-flet/`. La raíz del repo contiene `frontend-flet/`, `.gitignore`, `crear_proyecto.ps1` (script que generó la estructura), `.vscode/` y este `AGENTS.md`.
- Punto de entrada: `frontend-flet/main.py`.
- Dependencias en `frontend-flet/requirements.txt` (flet, flet-desktop, httpx, pydantic-settings, python-dotenv, etc.). Existe un `venv/` dentro de `frontend-flet/` (ignorada por git).
- Configuración por variables de entorno en `frontend-flet/.env`, leídas por `core/config.py` con `pydantic_settings.BaseSettings`: `URL_BACKEND`, `PASSWORD_RESET_DEFAULT`, `URL_PUBLICA`. Usar siempre `from core.config import settings` y `settings.URL_BACKEND`; nunca hardcodear URLs ni secretos.

## Arquitectura y estructura

```
frontend-flet/
├── main.py               # Entry: login → Layout principal; controla el flujo entre pantallas
├── core/                 # config.py (settings/.env), constants.py; routes.py y theme.py existen vacíos
├── components/           # UI reutilizable: layout.py, sidebar.py, alerts.py (Toast), datapicker.py
│                         # (buttons.py, inputs.py, data_table.py, loading.py, modal.py, navbar.py están vacíos;
│                         # los modales se definen dentro de views/, no en components/modal.py)
├── views/                # Una carpeta por módulo de negocio (legajos/, usuarios/, Gestion_haberes/, ...)
├── services/             # Archivos placeholder vacíos (api_client.py, auth_service.py, ...)
├── store/                # Archivos placeholder vacíos (app_state.py, auth_store.py, ui_store.py)
├── utils/                # formatters.py, permisos.py (helpers.py y validators.py vacíos)
└── tests/                # Vacío; hay scripts sueltos test_flet.py y test_servidor.py en la raíz
```

Capas (sepáralas y respetá su rol):

1. **Interfaz (componentes/vistas)**: clases Flet, normalmente subclases de `ft.Container`, que construyen controles en `build()` o en `__init__`.
2. **Presentación / flujo**: `main.py` y `components/layout.py` navegan entre vistas (`page.controls.clear()`, `layout.change_view(...)`); el `Sidebar` decide qué menú mostrar según permisos.
3. **Comunicación con backend**: llamadas HTTP `async` con `httpx.AsyncClient()` hechas **dentro de cada vista** (los archivos de `services/` y `store/` existen pero están vacíos; no inventes una capa nueva ni cambies el patrón sin que se pida).

Estado de sesión: se guarda en `page.session.store` (claves usadas: `"access_token"`, `"usuario"`). No crear store alternativo.

## Convenciones de código

- **Idioma**: español para nombres de clases, métodos, variables, rutas de vistas y textos de UI.
- **Naming**: clases `PascalCase` (`LegajosView`, `CrearLegajoView`); métodos/variables `snake_case` (`listar_legajos`, `api_crear`, `eliminar_item`); rutas de vistas en `snake_case` (`"crear_legajo"`, `"datos_fijos_liquidacion"`).
- Las vistas reciben `page` en `__init__` y guardan `self.page_ref = page` (o `self.page`); usá `self.page_ref` para `update()` y `run_task`.
- Dos patrones de handlers conviven en el proyecto; ambos son válidos y hay que seguir el del archivo vecino:
  - Lambdas síncronas que lanzan la corrutina con `self.page_ref.run_task(self.metodo_async, args)` (p. ej. botones "Nuevo"/"Eliminar" en `views/legajos/legajo_list_view.py`).
  - Asignación directa de métodos `async def` al evento: `on_click=self.guardar` (p. ej. `views/Gestion_haberes/conceptos/concepto_crear_editar_view.py`, `views/login/login_view.py`). Flet soporta handlers async nativos.
  - Los métodos de negocio/carga siempre son `async def`.
- Cada vista puede implementar `async def load(self)` (la llama `Layout.change_view` con `page.run_task`) y `set_mode(...)` cuando necesita parámetros de entrada.
- Navegación entre vistas del Layout: `self.page_ref.layout.change_view("nombre_vista", *args)`. Registrá vistas nuevas en el dict `Layout.views` de `components/layout.py` y, si corresponde, en el `Sidebar`.
- Estilos en línea con `ft.*` (no hay tema centralizado: `core/theme.py` está vacío). Colores frecuentes: fondo `#F1F5F9`, tarjetas blancas con borde `#E2E8F0`, botones primarios `#030B16`/`#091224` con `RoundedRectangleBorder(radius=0)`, sidebar `#040B1C`, texto secundario `#64748B`/`#0F172A`, éxito `#DCFCE7`/`#166534`, error `#FEE2E2`/`#991B1B`. Tablas: `ft.DataTable` con `heading_row_color="#E2E8F0"` y textos size 11.
- Formateo de números/fechas: reutilizar `utils/formatters.py` (`formatear_moneda`, `parsear_moneda`, `formatear_fecha`, `filtrar_decimal`); no reimplementar.
- Comentarios de sección con bloques `# =====` como en el código existente.

## Backend, API y datos

- El backend es FastAPI (la respuesta de error trae `detail`). **No modificar el backend ni la base de datos desde este workspace.**
- Endpoints usados por el frontend (orientativo, no exhaustivo; respetá sus paths, métodos, DTO y formatos de respuesta, no los cambies unilateralmente). Además de las subrutas con `{id}`, se usan: `/auth/login`, `/legajos`, `/legajos/{id}`, `/legajos/{id}/conceptos`, `/legajos/{id}/conceptos/{id}`, `/legajos/{id}/novedades`, `/categorias`, `/bancos`, `/modalidades`, `/conceptos`, `/conceptos/{id}`, `/clasificacion-conceptos`, `/datos-fijos-liquidacion`, `/datos-fijos-liquidacion/{id}`, `/liquidaciones`, `/liquidaciones/liquidar`, `/liquidaciones/datos-fijos/{id}`, `/novedades`, `/novedades/{id}`, `/historia-laboral`, `/usuarios`, `/usuarios/{id}`, `/usuarios/{id}/estado`, `/usuarios/{id}/password`, `/usuarios/{id}/password/reset`, `/roles`, `/permisos`, `/permisos/roles/{rol}`. Ante cualquier endpoint nuevo, verificar su uso en las vistas existentes antes de tocarlo.
- Patrón de llamada a seguir (copiar el de vistas vecinas):

```python
token = self.page_ref.session.store.get("access_token")
if not token:
    await self.toast.show(self.page_ref, "Sesión expirada", "error")
    return

headers = {"Authorization": f"Bearer {token}"}
url = f"{settings.URL_BACKEND}/legajos"

async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=headers, follow_redirects=True)

if response.status_code == 401:
    await self.toast.show(self.page_ref, "Token inválido o expirado", "error")
    return
if response.status_code != 200:
    await self.toast.show(self.page_ref, f"Error API: {response.status_code}", "error")
    return
data = response.json()
```


- Manejá siempre: sin token (token faltante/expirado), `status_code` distinto del esperado (200/201 según el endpoint; mostrar `data.get("detail")` cuando haya), excepciones de red (`try/except` + toast), y estado de carga (deshabilitar el botón y mostrar `ft.ProgressRing` mientras se espera, como en `LoginView`).
- Errores y confirmaciones al usuario: usar el componente `Toast` de `components/alerts.py` (`await self.toast.show(page, mensaje, "error"|"success"|"info")`), agregado a `page.overlay` o al `ft.Stack` de la vista según el patrón de la vista.

## Autenticación y permisos

- Login: `POST {URL_BACKEND}/auth/login` con `{"username", "password"}`. La respuesta tiene `access_token`, `usuario` y `requiere_cambio_password`; se guardan en `page.session.store` (`"access_token"`, `"usuario"`).
- El objeto `usuario` contiene `id`, `nombre`, `apellido`, `rol` y `permisos` (lista de códigos).
- Verificación de permisos con `utils/permisos.py`: `tiene_permiso(page, "CODIGO_PERMISO")`. El rol `SUPERADMINISTRADOR` tiene acceso total.
- Los códigos siguen el patrón `RECURSO_(ACCEDER|CREAR|EDITAR|ELIMINAR)`, p. ej.: `LEGAJOS_ACCEDER`, `LEGAJOS_CREAR`, `LEGAJOS_EDITAR`, `LEGAJOS_ELIMINAR`, `LEGAJOS_HISTORIAL_LABORAL_ACCEDER`, `LEGAJOS_CONCEPTOS_APLICADOS_CREAR`, `SUELDOS_CONCEPTOS_ACCEDER`, `SUELDOS_CONCEPTOS_CREAR`, `SUELDOS_NOVEDADES_EDITAR`, `SUELDOS_LIQUIDACION_LIQUIDACIONES_ACCEDER`, `SUELDOS_LIQUIDACION_DATOS_FIJOS_ACCEDER`, `USUARIOS_GESTIONAR_USUARIOS_ACCEDER`, `USUARIOS_PERMISOS_ACCEDER`, `SEGURIDAD_AUDITORIA_ACCEDER`. La lista no es exhaustiva: buscar los códigos reales con `tiene_permiso(` en el módulo afectado antes de usar o crear permisos.
- Al cerrar sesión se elimina `"access_token"` del session store (ver logout en `Sidebar`). Respetá ese flujo.

## Reglas de trabajo

- **Mantener la arquitectura y estructura existentes**: no reorganizar carpetas, no introducir frameworks ni patrones nuevos (no MVC alternativo, no librerías de estado, no HTTP client distinto a httpx).
- **Reutilizar** antes de crear: `components/alerts.py` (Toast), `components/layout.py`, `components/sidebar.py`, `components/datapicker.py`, `utils/formatters.py`, `utils/permisos.py`, y los patrones de tabla/filtros/paginación de `views/legajos/legajo_list_view.py`. No duplicar lógica que ya exista en otro archivo.
- Para catálogos de **bancos, categorías y modalidades de liquidación**, reutilizar `CatalogosService` de `views/legajos/shared.py` (`cargar_bancos`/`cargar_categorias`/`cargar_modalidades_liquidacion`/`refresh`, cacheados en atributos de clase); no reimplementar esas llamadas a `/bancos`, `/categorias` ni `/modalidades` en vistas nuevas.
- **No agregar dependencias** ni tocar `requirements.txt` sin autorización explícita del usuario.
- **No modificar el backend ni la base de datos**; este workspace es solo el frontend.
- **No crear archivos temporales**, scripts de prueba desechables ni notas; no modificar archivos ajenos a la tarea solicitada (incluidos `venv/`, `.env`, `.gitignore` salvo pedido).
- **No hacer refactorizaciones, renombres ni mejoras no pedidas**: aunque haya duplicación o código desordenado (por ejemplo, funciones duplicadas en `utils/formatters.py` o archivos placeholder vacíos), solo se toca lo necesario para la tarea.
- **Trabajar únicamente sobre el alcance solicitado** y, al terminar, verificar los cambios: revisar que los archivos editados compilen (`python -m py_compile` con el venv de `frontend-flet/`) y que la navegación/permisos afectados sigan funcionando según el patrón existente.
- Si una tarea requiere salirse de estas reglas (nueva dependencia, cambio de endpoint, cambio estructural), preguntar antes de avanzar.
