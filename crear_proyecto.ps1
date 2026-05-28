# ============================================
# CREAR PROYECTO FRONTEND FLET
# ============================================

Write-Host "Creando estructura frontend-flet..." -ForegroundColor Green

# ROOT
mkdir frontend-flet

Set-Location frontend-flet

# ARCHIVOS ROOT
ni main.py
ni requirements.txt
ni .env
ni README.md

# =========================
# CORE
# =========================

mkdir core

ni core\config.py
ni core\routes.py
ni core\theme.py
ni core\constants.py

# =========================
# SERVICES
# =========================

mkdir services

ni services\api_client.py
ni services\auth_service.py
ni services\legajo_service.py
ni services\turno_service.py
ni services\liquidacion_service.py
ni services\novedades_service.py
ni services\usuario_service.py

# =========================
# STORE
# =========================

mkdir store

ni store\auth_store.py
ni store\app_state.py
ni store\ui_store.py

# =========================
# VIEWS
# =========================

mkdir views

# LOGIN
mkdir views\login

ni views\login\login_view.py
ni views\login\login_form.py

# DASHBOARD
mkdir views\dashboard

ni views\dashboard\dashboard_view.py

# LEGAJOS
mkdir views\legajos
mkdir views\legajos\components

ni views\legajos\legajo_list_view.py
ni views\legajos\legajo_detail_view.py
ni views\legajos\legajo_form.py

ni views\legajos\components\legajo_table.py
ni views\legajos\components\legajo_filters.py

# TURNOS
mkdir views\turnos
mkdir views\turnos\components

ni views\turnos\turnos_view.py
ni views\turnos\calendario_view.py

# LIQUIDACIONES
mkdir views\liquidaciones
mkdir views\liquidaciones\components

ni views\liquidaciones\liquidaciones_view.py
ni views\liquidaciones\recibo_view.py

# NOVEDADES
mkdir views\novedades
mkdir views\novedades\components

ni views\novedades\novedades_view.py

# USUARIOS
mkdir views\usuarios

ni views\usuarios\usuarios_view.py

# CONFIGURACION
mkdir views\configuracion

ni views\configuracion\configuracion_view.py

# =========================
# COMPONENTS
# =========================

mkdir components

ni components\navbar.py
ni components\sidebar.py
ni components\layout.py
ni components\data_table.py
ni components\modal.py
ni components\loading.py
ni components\alerts.py
ni components\buttons.py
ni components\inputs.py

# =========================
# UTILS
# =========================

mkdir utils

ni utils\formatters.py
ni utils\validators.py
ni utils\permissions.py
ni utils\helpers.py

# =========================
# ASSETS
# =========================

mkdir assets
mkdir assets\images
mkdir assets\icons
mkdir assets\styles

# =========================
# TESTS
# =========================

mkdir tests

# =========================
# VENV
# =========================

python -m venv venv

# =========================
# MAIN.PY
# =========================

@'
import flet as ft

def main(page: ft.Page):

    page.title = "Sistema Integral"

    page.add(
        ft.Text("Frontend Flet funcionando")
    )

ft.app(target=main)
'@ | Set-Content main.py

# =========================
# README
# =========================

@'
# Frontend Flet

Sistema Integral de Gestión.
'@ | Set-Content README.md

# =========================
# FIN
# =========================

Write-Host ""
Write-Host "Proyecto creado correctamente." -ForegroundColor Cyan
Write-Host ""
Write-Host "Ahora ejecutar:" -ForegroundColor Yellow
Write-Host ""
Write-Host "cd frontend-flet"
Write-Host ".\venv\Scripts\activate"
Write-Host "pip install flet requests python-dotenv"
Write-Host "flet run --web main.py"