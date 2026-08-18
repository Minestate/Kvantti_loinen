import httpx
from bs4 import BeautifulSoup
import re
import zlib
import os
import json

BLOCK_SIZE = 1024  # 1 Kilotavu
OUTPUT_DIR = "packed_ads"

# --- 1. TARKAT AD-BLOCK & OVERLAY SÄÄNNÖT ---

# Laajennetut mainos- ja seurantaverkkojen patternit (EasyList-pohjainen)
EASYLIST_PATTERNS = [
    r'/ad[s]?/', r'/banner[s]?/', r'/pop[up|under]?', r'doubleclick\.net',
    r'googlesyndication\.com', r'googleadservices\.com', r'adnxs\.com',
    r'outbrain\.com', r'taboola\.com', r'rubiconproject\.com', r'criteo\.com',
    r'amazon-adsystem\.com', r'adform\.net', r'casalemedia\.com'
]

# Standardit IAB-mainoskoot (leveys x korkeus)
IAB_AD_SIZES = [
    (728, 90),   # Leaderboard
    (300, 250),  # Medium Rectangle
    (160, 600),  # Wide Skyscraper
    (300, 600),  # Half Page
    (320, 50)    # Mobile Leaderboard
]

# --- PAKKAUSLOGIIKKA (1 KT TUPLA) ---

def pack_data_twice(data: bytes) -> bytes:
    return zlib.compress(zlib.compress(data))

def process_and_save_chunks(raw_bytes: bytes, target_dir: str):
    os.makedirs(target_dir, exist_ok=True)
    chunks = [raw_bytes[i:i + BLOCK_SIZE] for i in range(0, len(raw_bytes), BLOCK_SIZE)]
    
    print(f"  -> Data pilkottu {len(chunks)} kpl 1 kt:n lohkoihin.")
    for idx, chunk in enumerate(chunks):
        packed = pack_data_twice(chunk)
        file_path = os.path.join(target_dir, f"chunk_{idx}.pkg")
        with open(file_path, "wb") as f:
            f.write(packed)
        print(f"     [Tallennettu] {file_path} ({len(chunk)} B -> {len(packed)} B)")

# --- LAAJENNETTU EDISTYNYT KERÄÄJÄ ---

def analyze_and_extract_ads(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    print(f"\n[1] Ladataan ja analysoidaan kohdesivu: {url}")
    try:
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=10.0)
    except Exception as e:
        print(f"Virhe ladattaessa sivua: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    extracted_data = {
        "source_url": url,
        "matched_banners": [],
        "detected_popups_and_overlays": []
    }

    # A. BANNERIT JA MAINOSLINKIT (URL + IAB-KOOT)
    for tag in soup.find_all(['iframe', 'img', 'a', 'div']):
        src = tag.get('src') or tag.get('href') or tag.get('data-src') or ''
        width = tag.get('width')
        height = tag.get('height')

        # 1. Osoite-pohjainen täsmäys
        matched_pattern = next((p for p in EASYLIST_PATTERNS if re.search(p, src, re.IGNORECASE)), None)
        
        # 2. Kokopohjainen IAB-täsmäys
        is_iab_size = False
        if width and height:
            try:
                size_tuple = (int(width), int(height))
                if size_tuple in IAB_AD_SIZES:
                    is_iab_size = True
            except ValueError:
                pass

        if matched_pattern or is_iab_size:
            extracted_data["matched_banners"].append({
                'element': tag.name,
                'url': src,
                'reason': 'EasyList URL Match' if matched_pattern else 'IAB Size Match',
                'dimensions': f"{width}x{height}" if width and height else "N/A"
            })

    # B. OVERLAY- JA POP-UP ELEMENTIT (CSS + DOM -RAKENNE)
    for element in soup.find_all(['div', 'section', 'aside', 'dialog']):
        style = element.get('style', '').lower()
        classes = " ".join(element.get('class', [])).lower()
        elem_id = element.get('id', '').lower()

        # Etsitään CSS-ominaisuuksia, jotka ankkuroivat elementin ruudun päälle
        is_fixed_or_abs = 'position:fixed' in style.replace(' ', '') or 'position:absolute' in style.replace(' ', '')
        has_high_zindex = 'z-index' in style and any(char.isdigit() for char in style)
        
        # Etsitään luokka- tai ID-avainsanoja
        popup_keywords = ['modal', 'popup', 'pop-up', 'overlay', 'consent', 'cookie', 'newsletter', 'banner']
        has_keyword = any(kw in classes or kw in elem_id for kw in popup_keywords)

        if (is_fixed_or_abs and has_high_zindex) or has_keyword:
            extracted_data["detected_popups_and_overlays"].append({
                'tag': element.name,
                'id': elem_id,
                'class': classes,
                'inline_style': style[:100],  # Rajataan tyylimääreitä
                'snippet': element.get_text(strip=True)[:100]
            })

    print(f"\n[2] Löydöt:")
    print(f"  - Bannerit / Mainokset: {len(extracted_data['matched_banners'])} kpl")
    print(f"  - Pop-upit / Overlayt: {len(extracted_data['detected_popups_and_overlays'])} kpl")

    # C. PAKKAUSLOGIIKKA (1 KT LOHKOT -> TUPLAPAKATTU)
    raw_bytes = json.dumps(extracted_data, ensure_ascii=False, indent=2).encode('utf-8')
    print(f"\n[3] Suoritetaan 1 kt tuplapakkaus kerätylle datalle...")
    process_and_save_chunks(raw_bytes, OUTPUT_DIR)

if __name__ == "__main__":
    target_site = "https://example.com"
    analyze_and_extract_ads(target_site)