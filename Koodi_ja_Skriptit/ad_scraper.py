import httpx
from bs4 import BeautifulSoup
import re

# Tunnettuja mainosverkkoja ja -avainsanoja suodatusta varten (AdBlock-logiikka)
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

# Standardit IAB-mainoskoot (leveys x korkeus)
STANDARD_AD_SIZES = ["728x90", "300x250", "160x600", "320x50", "300x600"]

def inspect_page_for_ads(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Ladataan sivua: {url}...")
    try:
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=10.0)
    except Exception as e:
        print(f"Virhe ladattaessa sivua: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    found_ads = []
    found_popups = []

    # 1. ETSITÄÄN MAINOS-IFRAMET JA KUVA-BANNERIT
    for tag in soup.find_all(['iframe', 'img', 'a']):
        src = tag.get('src') or tag.get('href') or ''
        
        # Tarkistetaan täsmääkö osoite mainoskuvioihin
        if any(re.search(pattern, src, re.IGNORECASE) for pattern in AD_PATTERNS):
            found_ads.append({
                'type': tag.name,
                'url': src,
                'alt': tag.get('alt', '')
            })

    # 2. ETSITÄÄN POP-UP -ELEMENTIT JA OVERLAY-MODAALIT (CSS-luokat ja -id:t)
    popup_indicators = ['popup', 'pop-up', 'modal', 'overlay', 'newsletter-signup', 'banner-ad']
    
    for element in soup.find_all(['div', 'section', 'aside']):
        element_id = element.get('id', '')
        element_classes = " ".join(element.get('class', []))
        
        combined_attr = f"{element_id} {element_classes}".lower()
        
        if any(indicator in combined_attr for indicator in popup_indicators):
            found_popups.append({
                'tag': element.name,
                'id': element_id,
                'class': element_classes,
                'text_preview': element.get_text(strip=True)[:100]  # Ensimmäiset 100 merkkiä tekstistä
            })

    # TULOSTETAAN LÖYDÖT
    print(f"\n--- MAINOSBANNERIT JA -LINKIT ({len(found_ads)} kpl) ---")
    for ad in found_ads:
        print(f"[{ad['type'].upper()}] {ad['url']}")

    print(f"\n--- POP-UP JA MODAALI-ELEMENTIT ({len(found_popups)} kpl) ---")
    for popup in found_popups:
        print(f"[{popup['tag']}] ID: '{popup['id']}' | Class: '{popup['class']}'")
        print(f"  Teksti: {popup['text_preview']}...\n")

if __name__ == "__main__":
    # Testaa haluamallasi osoitteella
    target_url = "https://example.com" 
    inspect_page_for_ads(target_url)