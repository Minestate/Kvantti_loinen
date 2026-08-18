import httpx
from bs4 import BeautifulSoup
import re
import zlib
import os
import json

BLOCK_SIZE = 1024  # 1 Kilotavu (1024 tavua)
OUTPUT_DIR = "packed_ads"

# Tunnettuja mainosverkkoja ja -avainsanoja suodatusta varten
AD_PATTERNS = [
    r'doubleclick\.net',
    r'googlesyndication\.com',
    r'adservice\.google\.',
    r'adnxs\.com',
    r'/ads/',
    r'/banners/',
    r'popunder',
    r'popup'
]

POPUP_INDICATORS = ['popup', 'pop-up', 'modal', 'overlay', 'newsletter-signup', 'banner-ad']

# --- PAKKAUSLOGIIKKA ---

def pack_data_twice(data: bytes) -> bytes:
    """Pakkaa 1 kt:n datalohkon kaksi kertaa sisäkkäin."""
    first_compressed = zlib.compress(data)
    second_compressed = zlib.compress(first_compressed)
    return second_compressed

def process_and_save_chunks(raw_bytes: bytes, target_dir: str):
    """Pilkkoo raakADatan 1 kt:n osiin, tuplapakkaa ja tallentaa ne."""
    os.makedirs(target_dir, exist_ok=True)
    
    # Pilkotaan täsmälleen 1024 tavun eriin
    chunks = [raw_bytes[i:i + BLOCK_SIZE] for i in range(0, len(raw_bytes), BLOCK_SIZE)]
    
    print(f"  -> Data pilkottu {len(chunks)} kpl 1 kt:n lohkoihin.")
    
    for idx, chunk in enumerate(chunks):
        packed_bytes = pack_data_twice(chunk)
        file_path = os.path.join(target_dir, f"chunk_{idx}.pkg")
        
        with open(file_path, "wb") as f:
            f.write(packed_bytes)
            
        print(f"     [Tallennettu] {file_path} (Alkuperäinen: {len(chunk)} B | Pakattu: {len(packed_bytes)} B)")

# --- KERÄÄJÄLOGIIKKA ---

def scrape_and_pack_ads(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"\n[1] Ladataan kohdesivu: {url}")
    try:
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=10.0)
    except Exception as e:
        print(f"Virhe ladattaessa sivua: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    extracted_data = {
        "source_url": url,
        "ads": [],
        "popups": []
    }

    # 1. Mainokset & Bannerit
    for tag in soup.find_all(['iframe', 'img', 'a']):
        src = tag.get('src') or tag.get('href') or ''
        if any(re.search(pattern, src, re.IGNORECASE) for pattern in AD_PATTERNS):
            extracted_data["ads"].append({
                'type': tag.name,
                'url': src,
                'alt': tag.get('alt', '')
            })

    # 2. Pop-upit & Modaalit
    for element in soup.find_all(['div', 'section', 'aside']):
        element_id = element.get('id', '')
        element_classes = " ".join(element.get('class', []))
        combined_attr = f"{element_id} {element_classes}".lower()
        
        if any(indicator in combined_attr for indicator in POPUP_INDICATORS):
            extracted_data["popups"].append({
                'tag': element.name,
                'id': element_id,
                'class': element_classes,
                'content_snippet': element.get_text(strip=True)[:150]
            })

    print(f"\n[2] Löydöt: {len(extracted_data['ads'])} mainosta, {len(extracted_data['popups'])} pop-upia.")

    # 3. Muunnetaan kerätty JSON-data raakabytteiksi ja ajetaan pakkaus
    raw_json_bytes = json.dumps(extracted_data, ensure_ascii=False, indent=2).encode('utf-8')
    
    print(f"\n[3] Suoritetaan 1 kt tuplapakkaus kerätylle datalle...")
    process_and_save_chunks(raw_json_bytes, OUTPUT_DIR)

if __name__ == "__main__":
    # Syötä tähän haluamasi kohdesivusto
    target_site = "https://example.com"
    scrape_and_pack_ads(target_site)