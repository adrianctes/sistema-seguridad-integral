from datetime import date, datetime


def filtrar_decimal(texto: str) -> str:
    """
    Permite solo números y un único separador decimal.
    Convierte la coma a punto.

    Ejemplos:
    "12a3"      -> "123"
    "10,5"      -> "10.5"
    "1.2.3"     -> "1.23"
    "10,25.50"  -> "10.2550"
    """

    if not texto:
        return ""

    permitido = ""
    separador = False

    for c in texto:
        if c.isdigit():
            permitido += c

        elif c in [".", ","] and not separador:
            permitido += "."
            separador = True

    return permitido

def parsear_moneda(texto: str) -> float:
    if not texto:
        return 0.0

    return float(
        texto.strip()
             .replace(".", "")
             .replace(",", ".")
    )


def formatear_moneda(valor: float) -> str:
    return (
        f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

def formatear_moneda(valor: float) -> str:
    """
    Convierte:
        25000     -> 25.000,00
        1500.5    -> 1.500,50
        10        -> 10,00
    """
    return (
        f"{float(valor):,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def parsear_moneda(texto: str) -> float:
    """
    Convierte:
        25.000,00 -> 25000.0
        1.500,50  -> 1500.5
        10,00     -> 10.0
    """
    if not texto:
        return 0.0

    return float(
        texto
        .replace(".", "")
        .replace(",", ".")
    )

def formatear_fecha(fecha : date):
          
        if fecha is None:
          return ""  
        return datetime.fromisoformat(fecha).strftime("%d/%m/%Y")