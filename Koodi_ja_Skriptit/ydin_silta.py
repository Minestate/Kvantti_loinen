from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver

# Salli portin uudelleenkäyttö
socketserver.TCPServer.allow_reuse_address = True

class PerustaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Tässä on oltava sisennys (4 välilyöntiä)
        if self.path == '/api/rekisteri':
            try:
                with open("rekisteri.txt", "r") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            # Kaikki muu polku menee oletusarvoisesti eteenpäin
            super().do_GET()

server_address = ('localhost', 8000)
httpd = HTTPServer(server_address, PerustaHandler)
print("[EMOLEVY] Silta pystyssä, portti 8000, API-reititys korjattu.")
httpd.serve_forever()
