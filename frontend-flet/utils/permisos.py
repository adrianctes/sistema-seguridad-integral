def tiene_permiso(page, codigo: str) -> bool:

    usuario = page.session.store.get("usuario")

    if not usuario:
        return False

    # SUPERADMINISTRADOR tiene acceso total
    if usuario.get("rol") == "SUPERADMINISTRADOR":
        return True

    permisos = usuario.get("permisos", [])

    return codigo in permisos