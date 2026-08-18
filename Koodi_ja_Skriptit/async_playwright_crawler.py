import asyncio
import os
import json
import zlib
import re
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# --- ASETUKSET ---
BLOCK_SIZE = 1024  # 1 Kt (1024 tavua)
OUTPUT_DIR = "packed_ads_async"
LOG_DIR = "packed_logs"
SERVER_URL = "http://localhost:3000/api/bot-data"
RUN_INTERVAL_SECONDS = 3600  # Ajo-välipyyntö (1 tunti)

# --- LOKITUSJÄRJESTELMÄ ---
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# --- SÄÄNNÖT POP-UPEILLE JA MAINOKSILLE ---
POPUP_CLOSE_SELECTORS = [
    "button[id*='accept']", "button[class*='accept']",
    "button[id*='cookie']", ".cookie-consent-accept",
    "button[aria-label='Close']", ".modal-close",
    "[data-testid='close-button']", ".close-button"
]

EASYLIST_PATTERNS = [
    r'/ad[s]?/', r'/banner[s]?/', r'/pop[up|under]?', r'doubleclick\.net',
    r'googlesyndication\.com', r'googleadservices\.com', r'adnxs\.com',
    r'outbrain\.com', r'taboola\.com', r'criteo\.com'
]

# --- PAKKAUSLOGIIKKA (1 KT TUPLA) ---
def pack_data_twice(data: bytes) -> bytes:
    return zlib.compress(zlib.compress(data))

def process_and_save_chunks(raw_bytes: bytes, target_dir: str, prefix: str):
    os.makedirs(target_dir, exist_ok=True)
    chunks = [raw_bytes[i:i + BLOCK_SIZE] for i in range(0, len(raw_bytes), BLOCK_SIZE)]
    
    for idx, chunk in enumerate(chunks):
        packed = pack_data_twice(chunk)
        file_path = os.path.join(target_dir, f"{prefix}_chunk_{idx}.pkg")
        with open(file_path, "wb") as f:
            f.write(packed)

def archive_log_file():
    if os.path.exists(log_filename):
        with open(log_filename, "rb") as f:
            log_bytes = f.read()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        process_and_save_chunks(log_bytes, LOG_DIR, f"log_{timestamp}")
        logging.info(f"Lokitiedosto pakattu ja säilötty kansioon {LOG_DIR}.")

# --- LÄHETYS SERVER.JS PALVELIMELLE ---
async def send_to_server(client: httpx.AsyncClient, payload: dict):
    try:
        response = await client.post(SERVER_URL, json=payload, timeout=5.0)
        if response.status_code == 200:
            logging.info("  -> [API] Tulokset lähetetty server.js-palvelimelle.")
    except Exception as e:
        logging.warning(f"  ! [API] Palvelinlähetys epäonnistui: {e}")

# --- PLAYWRIGHT SELAINAUTOMAATIO-BOTTI ---
class PlaywrightAdCrawlerBot:
    def __init__(self, start_url: str, max_pages: int = 5):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        self.visited = set()
        self.page_counter = 0

    async def handle_popups(self, page):
        """Etsii ja sulkee automaattisesti vastaan tulevat pop-upit."""
        for selector in POPUP_CLOSE_SELECTORS:
            try:
                close_btn = page.locator(selector).first
                if await close_btn.is_visible(timeout=800):
                    logging.info(f"  [POP-UP] Suljetaan pop-up elementillä: {selector}")
                    await close_btn.click()
                    await page.wait_for_timeout(500)
            except Exception:
                continue

    async def analyze_and_process(self, page, url: str, http_client: httpx.AsyncClient):
        self.page_counter += 1
        current_idx = self.page_counter
        logging.info(f"[{current_idx}/{self.max_pages}] Analysoidaan selainnäkymä: {url}")

        # Suljetaan pop-upit ennen analyysiä
        await self.handle_popups(page)

        # Haetaan sivun HTML selainympäristöstä
        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'html.parser')

        extracted_data = {
            "source_url": url,
            "matched_banners": [],
            "detected_popups_and_overlays": []
        }

        # 1. Mainokset
        for tag in soup.find_all(['iframe', 'img', 'a', 'div']):
            src = tag.get('src') or tag.get('href') or ''
            if any(re.search(p, src, re.IGNORECASE) for p in EASYLIST_PATTERNS):
                extracted_data["matched_banners"].append({'element': tag.name, 'url': src})

        # 2. Pop-upit ja overlayt
        for element in soup.find_all(['div', 'section', 'dialog']):
            classes = " ".join(element.get('class', [])).lower()
            elem_id = element.get('id', '').lower()
            if any(kw in classes or kw in elem_id for kw in ['modal', 'popup', 'overlay', 'consent']):
                extracted_data["detected_popups_and_overlays"].append({
                    'tag': element.name, 'id': elem_id, 'class': classes
                })

        logging.info(f"  -> Löydetty: {len(extracted_data['matched_banners'])} banneria, {len(extracted_data['detected_popups_and_overlays'])} pop-upia.")

        # A: Lähetys server.js:lle
import asyncio
import os
import json
import zlib
import re
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# --- ASETUKSET ---
BLOCK_SIZE = 1024  # 1 Kt (1024 tavua)
OUTPUT_DIR = "packed_ads_async"
LOG_DIR = "packed_logs"
SERVER_URL = "http://localhost:3000/api/bot-data"
RUN_INTERVAL_SECONDS = 3600  # Ajo-välipyyntö (1 tunti)

# --- KOHDEOSOITELISTA ---
TARGET_SITES = [
    "https://www.iltalehti.fi",
    "https://www.is.fi",
    "https://www.hs.fi",
    "https://yle.fi/uutiset",
    "https://www.bbc.com/news"
]

# --- LOKITUSJÄRJESTELMÄ ---
os.makedirs("logs", exist_ok=True)
log_filename = f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# --- SÄÄNNÖT POP-UPEILLE JA MAINOKSILLE ---
POPUP_CLOSE_SELECTORS = [
    "button[id*='accept']", "button[class*='accept']",
    "button[id*='cookie']", ".cookie-consent-accept",
    "button[aria-label='Close']", ".modal-close",
    "[data-testid='close-button']", ".close-button",
    "#cmpbntyestxt", "#almp-consent-accept-all"
]

EASYLIST_PATTERNS = [
    r'/ad[s]?/', r'/banner[s]?/', r'/pop[up|under]?', r'doubleclick\.net',
    r'googlesyndication\.com', r'googleadservices\.com', r'adnxs\.com',
    r'outbrain\.com', r'taboola\.com', r'criteo\.com'
]

# --- PAKKAUSLOGIIKKA (1 KT TUPLA) ---
def pack_data_twice(data: bytes) -> bytes:
    return zlib.compress(zlib.compress(data))

def process_and_save_chunks(raw_bytes: bytes, target_dir: str, prefix: str):
    os.makedirs(target_dir, exist_ok=True)
    chunks = [raw_bytes[i:i + BLOCK_SIZE] for i in range(0, len(raw_bytes), BLOCK_SIZE)]
    
    for idx, chunk in enumerate(chunks):
        packed = pack_data_twice(chunk)
        file_path = os.path.join(target_dir, f"{prefix}_chunk_{idx}.pkg")
        with open(file_path, "wb") as f:
            f.write(packed)

def archive_log_file():
    if os.path.exists(log_filename):
        with open(log_filename, "rb") as f:
            log_bytes = f.read()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        process_and_save_chunks(log_bytes, LOG_DIR, f"log_{timestamp}")
        logging.info(f"Lokitiedosto pakattu ja säilötty kansioon {LOG_DIR}.")

# --- LÄHETYS SERVER.JS PALVELIMELLE ---
async def send_to_server(client: httpx.AsyncClient, payload: dict):
    try:
        response = await client.post(SERVER_URL, json=payload, timeout=5.0)
        if response.status_code == 200:
            logging.info("  -> [API] Tulokset lähetetty server.js-palvelimelle.")
    except Exception as e:
        logging.warning(f"  ! [API] Palvelinlähetys epäonnistui: {e}")

# --- PLAYWRIGHT SELAINAUTOMAATIO-BOTTI ---
class PlaywrightAdCrawlerBot:
    def __init__(self, start_url: str, max_pages: int = 25):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        self.visited = set()
        self.page_counter = 0

    async def handle_popups(self, page):
        """Etsii ja sulkee automaattisesti vastaan tulevat pop-upit."""
        for selector in POPUP_CLOSE_SELECTORS:
            try:
                close_btn = page.locator(selector).first
                if await close_btn.is_visible(timeout=800):
                    logging.info(f"  [POP-UP] Suljetaan pop-up elementillä: {selector}")
                    await close_btn.click()
                    await page.wait_for_timeout(500)
            except Exception:
                continue

    async def analyze_and_process(self, page, url: str, http_client: httpx.AsyncClient):
        self.page_counter += 1
        current_idx = self.page_counter
        logging.info(f"[{current_idx}/{self.max_pages}] Analysoidaan selainnäkymä: {url}")

        await self.handle_popups(page)

        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'html.parser')

        extracted_data = {
            "source_url": url,
            "matched_banners": [],
            "detected_popups_and_overlays": []
        }

        # Mainokset
        for tag in soup.find_all(['iframe', 'img', 'a', 'div']):
            src = tag.get('src') or tag.get('href') or ''
            if any(re.search(p, src, re.IGNORECASE) for p in EASYLIST_PATTERNS):
                extracted_data["matched_banners"].append({'element': tag.name, 'url': src})

        # Pop-upit ja overlayt
        for element in soup.find_all(['div', 'section', 'dialog']):
            classes = " ".join(element.get('class', [])).lower()
            elem_id = element.get('id', '').lower()
            if any(kw in classes or kw in elem_id for kw in ['modal', 'popup', 'overlay', 'consent']):
                extracted_data["detected_popups_and_overlays"].append({
                    'tag': element.name, 'id': elem_id, 'class': classes
                })

        logging.info(f"  -> Löydetty: {len(extracted_data['matched_banners'])} banneria, {len(extracted_data['detected_popups_and_overlays'])} pop-upia.")

        await send_to_server(http_client, extracted_data)

        raw_bytes = json.dumps(extracted_data, ensure_ascii=False, indent=2).encode('utf-8')
        site_prefix = self.base_domain.replace(".", "_")
        process_and_save_chunks(raw_bytes, OUTPUT_DIR, f"pw_{site_prefix}_{current_idx}")

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            async with httpx.AsyncClient() as http_client:
                queue = [self.start_url]

                while queue and self.page_counter < self.max_pages:
                    current_url = queue.pop(0)
                    if current_url in self.visited:
                        continue

                    self.visited.add(current_url)
                    
                    try:
                        await page.goto(current_url, wait_until="domcontentloaded", timeout=15000)
                        await self.analyze_and_process(page, current_url, http_client)

                        links = await page.locator("a[href]").element_handles()
                        for link in links:
                            href = await link.get_attribute("href")
                            if href:
                                full_url = urljoin(current_url, href)
                                if urlparse(full_url).netloc == self.base_domain and full_url not in self.visited:
                                    queue.append(full_url)

                    except Exception as e:
                        logging.error(f"Virhe avattaessa sivua {current_url}: {e}")

            await browser.close()

# --- AUTOMAATTISEN AJOITUKSEN SILMUKKA ---
async def autonomous_loop():
    while True:
        for start_site in TARGET_SITES:
            logging.info(f"\n=== PLAYWRIGHT-BOTTI: Aloitetaan kohdesivusto {start_site} (25 sivua) ===")
            bot = PlaywrightAdCrawlerBot(start_url=start_site, max_pages=25)
            await bot.run()
            
            archive_log_file()
            
        logging.info(f"Kaikki sivustot käyty läpi. Odotetaan {RUN_INTERVAL_SECONDS / 60:.0f} minuuttia seuraavaan kierrokseen...\n")
        await asyncio.sleep(RUN_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(autonomous_loop())
    except KeyboardInterrupt:
        logging.info("Botti pysäytetty manuaalisesti.")