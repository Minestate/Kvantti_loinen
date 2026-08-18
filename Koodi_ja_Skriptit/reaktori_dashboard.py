import http.server
import socketserver
import json
import os

PORT = 8080

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Luetaan ledger ja näytetään se HTML-muodossa
        data_list = []
        if os.path.exists("ledger.json"):
            with open("ledger.json", "r") as f:
                data_list = [json.loads(line) for line in f if line.strip()]
        
        html = "<html><body><h1>Perusta Dashboard</h1><ul>"
        for entry in data_list:
            html += f"<li>{entry}</li>"
        html += "</ul></body></html>"
        
        self.wfile.write(html.encode())

with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
    print(f"Palvelin käynnissä portissa {PORT}")
    httpd.serve_forever()
