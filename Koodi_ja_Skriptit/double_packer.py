import zlib
import os

BLOCK_SIZE = 1024  # 1 Kilotavu (1024 tavua)

def pack_data_twice(data: bytes) -> bytes:
    """
    Pakkaa 1 kt:n datalohkon kaksi kertaa sisäkkäin.
    """
    # 1. Ensimmäinen pakkaus (sisempi)
    first_compressed = zlib.compress(data)
    
    # 2. Toinen pakkaus (ulompi, jonka sisälle ensimmäinen pakataan)
    second_compressed = zlib.compress(first_compressed)
    
    return second_compressed

def unpack_data_twice(double_compressed_data: bytes) -> bytes:
    """
    Purkaa ulomman pakkauksen, ja sen sisältä paljastuvan ensimmäisen pakkauksen.
    """
    # 1. Puretaan toinen (ulompi) pakkaus
    first_level = zlib.decompress(double_compressed_data)
    
    # 2. Puretaan ensimmäinen (sisempi) pakkaus
    original_data = zlib.decompress(first_level)
    
    return original_data

def process_and_save_ad_data(raw_data: bytes, output_dir: str = "packed_ads"):
    """
    Pilkkoo datan 1 kt:n osiin, pakkaa ne tuplana ja tallentaa levylle.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Pilkotaan data 1024 tavun (1 kt) eriin
    chunks = [raw_data[i:i + BLOCK_SIZE] for i in range(0, len(raw_data), BLOCK_SIZE)]
    
    print(f"Syöte pilkottu {len(chunks)} kpl 1 kt:n lohkoihin.")
    
    for idx, chunk in enumerate(chunks):
        # Pakataan 1 kt lohko kaksi kertaa
        packed_bytes = pack_data_twice(chunk)
        
        file_path = os.path.join(output_dir, f"ad_chunk_{idx}.pkg")
        with open(file_path, "wb") as f:
            f.write(packed_bytes)
            
        print(f"Tallennettu paketti {idx}: {file_path} (Koko levyllä: {len(packed_bytes)} tavua)")

# --- TESTAUS / DEMO ---
if __name__ == "__main__":
    # Luodaan esimerkkidataa (esim. kerättyä mainos-HTML:ää tai kuvaa)
    sample_ad_text = ("MAINOS_DATA: Banneri #1042 - Koko 300x250 - URL: https://ads.example.com/banner.png\n" * 30).encode('utf-8')
    
    print(f"Alkuperäisen datan koko: {len(sample_ad_text)} tavua")
    
    # Suoritetaan tuplapakkaus 1 kt lohkoissa
    process_and_save_ad_data(sample_ad_text)
    
    # Testataan purkaminen ensimmäisen lohkon osalta
    with open("packed_ads/ad_chunk_0.pkg", "rb") as f:
        double_packed_sample = f.read()
        
    restored_chunk = unpack_data_twice(double_packed_sample)
    print("\n--- PURKUTESTI ---")
    print(f"Purettuko oikein 1 kt osio? {len(restored_chunk)} tavua.")
    print(f"Sisältönäyte: {restored_chunk[:100].decode('utf-8', errors='ignore')}...")