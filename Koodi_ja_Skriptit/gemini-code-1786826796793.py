# --- LÄHETETÄÄN TULOKSET NODE.JS PALVELIMELLE (VAIHTOEHTO A) ---
async def send_to_server(client: httpx.AsyncClient, payload: dict):
    server_url = "http://localhost:3000/api/bot-data"
    try:
        response = await client.post(server_url, json=payload, timeout=5.0)
        if response.status_code == 200:
            logging.info("  -> [API] Tulokset lähetetty onnistuneesti server.js-palvelimelle.")
    except Exception as e:
        logging.warning(f"  ! [API] Palvelinlähetys epäonnistui (server.js ei käynnissä?): {e}")