import os
import zlib
import json
import glob

def unpack_data_twice(packed_bytes: bytes) -> bytes:
    """Purkaa tuplapakatun zlib-datan."""
    return zlib.decompress(zlib.decompress(packed_bytes))

def read_and_combine_chunks(folder_path: str, prefix: str) -> str:
    """Etsii kaikki tietyn prefixin .pkg-palat, purkaa ja yhdistää ne järjestyksessä."""
    search_pattern = os.path.join(folder_path, f"{prefix}_chunk_*.pkg")
    chunk_files = glob.glob(search_pattern)

    if not chunk_files:
        print(f"[VIRHE] Paketteja ei löytynyt haulla: {search_pattern}")
        return ""

    # Järjestetään chunk-numeron mukaan (esim. _chunk_0.pkg, _chunk_1.pkg...)
    def get_chunk_idx(filename):
        try:
            return int(filename.split("_chunk_")[1].split(".pkg")[0])
        except ValueError:
            return 0

    sorted_files = sorted(chunk_files, key=get_chunk_idx)

    unpacked_bytes = bytearray()
    for filepath in sorted_files:
        with open(filepath, "rb") as f:
            packed_chunk = f.read()
            unpacked_chunk = unpack_data_twice(packed_chunk)
            unpacked_bytes.extend(unpacked_chunk)

    return unpacked_bytes.decode('utf-8', errors='replace')

def list_and_unpack_all():
    print("=== PKG-PAKETTIEN PURKAJA ===")
    
    # 1. Purataan sivulöydökset
    ads_dir = "packed_ads_async"
    if os.path.exists(ads_dir):
        pkg_files = glob.glob(os.path.join(ads_dir, "*.pkg"))
        prefixes = set(f.split("_chunk_")[0] for f in pkg_files)
        print(f"\n[SIVUDATA] Löydetty {len(prefixes)} eri sivukokonaisuutta ({len(pkg_files)} pakettia).")
        
        for prefix in sorted(prefixes):
            clean_prefix = os.path.basename(prefix)
            combined_json_str = read_and_combine_chunks(ads_dir, clean_prefix)
            try:
                data = json.loads(combined_json_str)
                print(f"\n--- Sivukokonaisuus: {clean_prefix} ---")
                print(f"URL: {data.get('source_url')}")
                print(f"Bannerit: {len(data.get('matched_banners', []))} kpl")
                print(f"Pop-upit: {len(data.get('detected_popups_and_overlays', []))} kpl")
            except Exception:
                print(f"Purku epäonnistui kohteelle {clean_prefix}")

    # 2. Puretaan lokitiedostot
    log_dir = "packed_logs"
    if os.path.exists(log_dir):
        log_files = glob.glob(os.path.join(log_dir, "*.pkg"))
        prefixes = set(f.split("_chunk_")[0] for f in log_files)
        print(f"\n[LOKIT] Löydetty {len(prefixes)} lokikokonaisuutta.")
        
        for prefix in sorted(prefixes):
            clean_prefix = os.path.basename(prefix)
            log_text = read_and_combine_chunks(log_dir, clean_prefix)
            print(f"\n--- Loki: {clean_prefix} ---")
            print(log_text[:300] + ("...\n[Tynkä]" if len(log_text) > 300 else ""))

if __name__ == "__main__":
    list_and_unpack_all()