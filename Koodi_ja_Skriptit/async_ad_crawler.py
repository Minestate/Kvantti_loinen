import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import zlib
import os
import json

BLOCK_SIZE = 1024  # 1 Kilotavu (1024 tavua)
OUTPUT_DIR = "packed_ads_async"
CONCURRENCY_LIMIT = 5  # Kuinka monta sivua ladataan samanaikaisesti

# --- AD-BLOCK & OVERLAY SÄÄNNÖT ---
EASYLIST_PATTERNS = [
    r'/ad[s]?/', r'/banner[s]?/', r'/pop[up|under]?', r'doubleclick\.net',
    r'googlesyndication\.com', r'googleadservices\.com', r'adnxs\.com',
    r'outbrain\.com', r'taboola\.com', r'rubiconproject\.com', r'criteo\.com',
    r'amazon-adsystem\.com', r'adform\.net', r'casalemedia\.com'
]

IAB_AD_SIZES = [(728, 90), (300, 250), (160, 600), (300, 600), (320, 50)]
POPUP_KEYWORDS = ['modal', 'popup', 'pop-up', 'overlay', 'consent', 'cookie', 'newsletter', 'banner']

# --- PAKKAUSLOGIIKKA (1 KT TUPLA) ---
def pack_data_twice(data: bytes) -> bytes:
    return zlib.compress(zlib.compress(data))

def process_and_save_chunks(raw_bytes: bytes, target_dir: str, page_idx: int):
    os.makedirs(target_dir, exist_ok=True)
    chunks = [raw_bytes[i:i + BLOCK_SIZE] for i in range(0, len(raw_bytes), BLOCK_SIZE)]
    
    for idx, chunk in enumerate(chunks):
        packed = pack_data_twice(chunk)
        file_path = os.path.join(target_dir, f"page_{page_idx}_chunk_{idx}.pkg")
        with open(file_path, "wb") as f:
            f.write(packed)

# --- ASYNKRONINEN CRAWLER ---
class AsyncAdCrawlerBot:
    def __init__(self, start_url: str, max_pages: int = 10):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        
        self.queue = asyncio.Queue()
        self.visited = set()
        self.page_counter = 0
        self.counter_lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    def is_internal_link(self, url: str) -> bool:
        netloc = urlparse(url).netloc
        return netloc == "" or netloc == self.base_domain

    async def fetch_and_analyze(self, client: httpx.AsyncClient, url: str, depth: int):
        async with self.semaphore:
            async with self.counter_lock:
                if self.page_counter >= self.max_pages or url in self.visited:
                    return
                self.visited.add(url)
                self.page_counter += 1
                current_idx = self.page_counter

            print(f"[{current_idx}/{self.max_pages}] [ASYNC] Ladataan (Syvyys {depth}): {url}")

            try:
                response = await client.get(url, timeout=10.0, follow_redirects=True)
            except Exception as e:
                print(f"  ! Virhe ladattaessa sivua {url}: {e}")
                return

            soup = BeautifulSoup(response.text, 'html.parser')
            extracted_data = {
                "source_url": url,
                "depth": depth,
                "matched_banners": [],
                "detected_popups_and_overlays": []
            }

            # 1. MAINOS- JA BANNERIANALYYSI
            for tag in soup.find_all(['iframe', 'img', 'a', 'div']):
                src = tag.get('src') or tag.get('href') or tag.get('data-src') or ''
                width, height = tag.get('width'), tag.get('height')

                matched_pattern = next((p for p in EASYLIST_PATTERNS if re.search(p, src, re.IGNORECASE)), None)
                is_iab = False
                if width and height:
                    try:
                        if (int(width), int(height)) in IAB_AD_SIZES:
                            is_iab = True
                    except ValueError:
                        pass

                if matched_pattern or is_iab:
                    extracted_data["matched_banners"].append({
                        'element': tag.name,
                        'url': src,
                        'reason': 'EasyList Match' if matched_pattern else 'IAB Size Match'
                    })

            # 2. OVERLAY- JA POP-UP ANALYYSI
            for element in soup.find_all(['div', 'section', 'aside', 'dialog']):
                style = element.get('style', '').lower()
                classes = " ".join(element.get('class', [])).lower()
                elem_id = element.get('id', '').lower()

                is_fixed_or_abs = 'position:fixed' in style.replace(' ', '') or 'position:absolute' in style.replace(' ', '')
                has_high_zindex = 'z-index' in style and any(char.isdigit() for char in style)
                has_keyword = any(kw in classes or kw in elem_id for kw in POPUP_KEYWORDS)

                if (is_fixed_or_abs and has_high_zindex) or has_keyword:
                    extracted_data["detected_popups_and_overlays"].append({
                        'tag': element.name,
                        'id': elem_id,
                        'class': classes,
                        'snippet': element.get_text(strip=True)[:80]
                    })

            print(f"  -> Sivu {current_idx} valmis: {len(extracted_data['matched_banners'])} banneria, {len(extracted_data['detected_popups_and_overlays'])} pop-upia.")

            # 3. 1 KT TUPLAPAKKAUS
            raw_bytes = json.dumps(extracted_data, ensure_ascii=False, indent=2).encode('utf-8')
            process_and_save_chunks(raw_bytes, OUTPUT_DIR, current_idx)

            # 4. UUSIEN LINKIEN LISÄYS JONOON
            for anchor in soup.find_all('a', href=True):
                full_url = urljoin(url, anchor['href'])
                if self.is_internal_link(full_url) and full_url not in self.visited:
                    await self.queue.put((full_url, depth + 1))

    async def run(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        print(f"=== KÄYNNISTETÄÄN ASYNKRONINEN CRAWLER ===")
        print(f"Start URL: {self.start_url} | Rinnakkaisuusraja: {CONCURRENCY_LIMIT}\n")

        await self.queue.put((self.start_url, 0))

        async with httpx.AsyncClient(headers=headers) as client:
            tasks = []
            while not self.queue.empty() and self.page_counter < self.max_pages:
                current_url, depth = await self.queue.get()
                if current_url not in self.visited:
                    task = asyncio.create_task(self.fetch_and_analyze(client, current_url, depth))
                    tasks.append(task)
                
                # Suoritetaan tehtäviä rinnakkain
                if len(tasks) >= CONCURRENCY_LIMIT:
                    await asyncio.gather(*tasks)
                    tasks = []

            if tasks:
                await asyncio.gather(*tasks)

        print(f"\n=== ASYNKRONINEN CRAWLING VALMIS: Käsitelty {self.page_counter} sivua. ===")

if __name__ == "__main__":
    start_site = "https://steamunlocked.org"
    bot = AsyncAdCrawlerBot(start_url=start_site, max_pages=10)
    asyncio.run(bot.run())