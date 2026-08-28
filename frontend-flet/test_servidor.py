from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        contenido = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Prueba</title>
        </head>
        <body>
            <h1>Servidor de impresión funcionando</h1>
            <p>Puerto 8060 OK</p>
        </body>
        </html>
        """

        contenido = contenido.encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(contenido))
        )

        self.end_headers()

        self.wfile.write(contenido)


servidor = HTTPServer(
    ("0.0.0.0", 8060),
    Handler
)

print("Servidor iniciado en puerto 8060")

servidor.serve_forever()