from dna_ydin import hae_ydin, injektoi
import http.server
import socketserver
import webbrowser
import os

# Asetetaan työhakemisto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

print(f"[PERUSTA] Käynnistetään paikallinen rajapinta portissa {PORT}...")
webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
