import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import html


class LiquidacionImpresion:

    servidor = None
    hilo = None
    datos = {}

    def __init__(self, page, data):

        self.page = page
        self.data = data

    # =====================================================
    # MOSTRAR
    # =====================================================

    async def mostrar(self):

        if not self.data:
            return

        liquidacion_id = self.data.get("id")

        if not liquidacion_id:
            return

        LiquidacionImpresion.datos[
            str(liquidacion_id)
        ] = self.data

        self.iniciar_servidor()

        url = (
            f"http://192.168.101.90:8060"
            f"/recibo/{liquidacion_id}"
        )

        print(
            f"Abriendo recibo: {url}"
        )

        await self.page.launch_url(
            url
        )
    # =====================================================
    # SERVIDOR
    # =====================================================

    def iniciar_servidor(self):

        if (
            LiquidacionImpresion.servidor
            is not None
        ):
            return

        handler = self.crear_handler()

        LiquidacionImpresion.servidor = HTTPServer(
            ("0.0.0.0", 8060),
            handler
        )

        LiquidacionImpresion.hilo = threading.Thread(
            target=LiquidacionImpresion.servidor.serve_forever,
            daemon=True
        )

        LiquidacionImpresion.hilo.start()

        print(
            "Servidor de impresión iniciado en puerto 8060"
        )

    # =====================================================
    # HANDLER
    # =====================================================

    def crear_handler(self):

        datos = LiquidacionImpresion.datos

        class ReciboHandler(BaseHTTPRequestHandler):

            def do_GET(self):

                path = urlparse(
                    self.path
                ).path

                if not path.startswith(
                    "/recibo/"
                ):

                    self.send_error(
                        404
                    )

                    return

                liquidacion_id = (
                    path.split("/")[-1]
                )

                data = datos.get(
                    liquidacion_id
                )

                if not data:

                    self.send_error(
                        404,
                        "Liquidación no encontrada"
                    )

                    return

                contenido = (
                    LiquidacionImpresion.generar_html(
                        data
                    )
                )

                contenido_bytes = (
                    contenido.encode("utf-8")
                )

                self.send_response(
                    200
                )

                self.send_header(
                    "Content-Type",
                    "text/html; charset=utf-8"
                )

                self.send_header(
                    "Content-Length",
                    str(len(contenido_bytes))
                )

                self.end_headers()

                self.wfile.write(
                    contenido_bytes
                )

            def log_message(
                self,
                format,
                *args
            ):
                pass

        return ReciboHandler

    # =====================================================
    # HTML
    # =====================================================

    @staticmethod
    def generar_html(data):

        filas = ""

        for item in data.get(
            "lineas",
            []
        ):

            filas += f"""
            <tr>

                <td>
                    {html.escape(
                        str(
                            item.get(
                                "codigo",
                                ""
                            )
                        )
                    )}
                </td>

                <td>
                    {html.escape(
                        str(
                            item.get(
                                "concepto",
                                ""
                            )
                        )
                    )}
                </td>

                <td class="numero">
                    {item.get("cantidad", 0)}
                </td>

                <td class="numero">
                    {item.get("valor", 0)}
                </td>

                <td class="numero">
                    {item.get("haber", 0)}
                </td>

                <td class="numero">
                    {item.get("retencion", 0)}
                </td>

                <td class="numero">
                    {item.get("total", 0)}
                </td>

            </tr>
            """

        return f"""
<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<title>
Liquidación {data.get("id", "")}
</title>

<style>

@page {{
    size: A4;
    margin: 15mm;
}}

* {{
    box-sizing: border-box;
}}

body {{

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    font-size: 12px;

    color: #111827;

    margin: 0;

    background: white;
}}

.recibo {{
    width: 100%;
}}

.titulo {{

    font-size: 20px;

    font-weight: bold;

    margin-bottom: 15px;
}}

.cabecera {{

    border: 1px solid #CBD5E1;

    padding: 12px;

    margin-bottom: 15px;

}}

.fila-cabecera {{

    display: flex;

    margin-bottom: 8px;

}}

.campo {{

    margin-right: 35px;
}}

.label {{

    font-weight: bold;

}}

table {{

    width: 100%;

    border-collapse: collapse;

}}

th {{

    background: #E2E8F0;

    border: 1px solid #CBD5E1;

    padding: 7px;

    text-align: left;

}}

td {{

    border: 1px solid #CBD5E1;

    padding: 6px;

}}

.numero {{

    text-align: right;

}}

.totales {{

    width: 350px;

    margin-left: auto;

    margin-top: 20px;

}}

.total {{

    display: flex;

    justify-content: space-between;

    padding: 6px;

}}

.neto {{

    border-top: 2px solid #111827;

    font-size: 16px;

    font-weight: bold;

    margin-top: 5px;

}}

.boton-imprimir {{

    position: fixed;

    top: 20px;

    right: 20px;

    padding: 10px 18px;

    font-size: 14px;

    border: none;

    border-radius: 5px;

    background: #2563EB;

    color: white;

    cursor: pointer;

}}

@media print {{

    .boton-imprimir {{

        display: none;

    }}

}}

</style>

</head>

<body>

<button
    class="boton-imprimir"
    onclick="window.print()"
>
    🖨 Imprimir
</button>

<div class="recibo">

    <div class="titulo">

        LIQUIDACIÓN DE HABERES

    </div>

    <div class="cabecera">

        <div class="fila-cabecera">

            <div class="campo">

                <span class="label">
                    Fecha:
                </span>

                {html.escape(
                    str(
                        data.get(
                            "fecha",
                            ""
                        )
                    )
                )}

            </div>

            <div class="campo">

                <span class="label">
                    Período:
                </span>

                {html.escape(
                    str(
                        data.get(
                            "periodo",
                            ""
                        )
                    )
                )}

            </div>

            <div class="campo">

                <span class="label">
                    Modalidad:
                </span>

                {html.escape(
                    str(
                        data.get(
                            "modalidad",
                            ""
                        )
                    )
                )}

            </div>

            <div class="campo">

                <span class="label">
                    Número:
                </span>

                {html.escape(
                    str(
                        data.get(
                            "numero",
                            ""
                        )
                    )
                )}

            </div>

        </div>

        <div class="fila-cabecera">

            <div class="campo">

                <span class="label">
                    Legajo:
                </span>

                {html.escape(
                    str(
                        data.get(
                            "legajo_id",
                            ""
                        )
                    )
                )}

            </div>

            <div class="campo">

                <span class="label">
                    Apellido y Nombre:
                </span>

                {html.escape(
                    str(
                        data.get(
                            "ayn",
                            ""
                        )
                    )
                )}

            </div>

        </div>

    </div>

    <h3>
        Conceptos liquidados
    </h3>

    <table>

        <thead>

            <tr>

                <th>Código</th>

                <th>Concepto</th>

                <th>Cantidad</th>

                <th>Valor</th>

                <th>Haberes</th>

                <th>Retención</th>

                <th>Total</th>

            </tr>

        </thead>

        <tbody>

            {filas}

        </tbody>

    </table>

    <div class="totales">

        <div class="total">

            <span>
                Total Haberes:
            </span>

            <strong>
                $ {data.get(
                    "total_haberes",
                    0
                )}
            </strong>

        </div>

        <div class="total">

            <span>
                Total Retenciones:
            </span>

            <strong>
                $ {data.get(
                    "total_retenciones",
                    0
                )}
            </strong>

        </div>

        <div class="total neto">

            <span>
                Neto a Cobrar:
            </span>

            <strong>
                $ {data.get(
                    "total_neto",
                    0
                )}
            </strong>

        </div>

    </div>

</div>

</body>

</html>
"""