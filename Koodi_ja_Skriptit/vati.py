from dna_ydin import hae_ydin, injektoi
import time
import math

def perusta_hq_vuorottelu():
    print("--- Perusta HQ: Monimuuttuja-tila aktivoitu ---")
    
    # Perusarvot
    base_lat, base_lon = 60.1699, 24.9384
    vaihe = 0
    
    try:
        while True:
            # Lasketaan 'kellonaika' tilan vaihtoa varten
            tila = vaihe % 3
            sekunnit = time.time()
            
            # Tila 0: Aurinkokellon diagnostiikka
            if tila == 0:
                latenssi = 0.1034 + (math.sin(sekunnit) * 0.01)
                print(f"[AURINKOKELLO] Latenssi: {latenssi:.4f}s | Tila: STABIILI")
            
            # Tila 1: Episteeminen kompassi
            elif tila == 1:
                tosi_suunta = (sekunnit * 5) % 360
                valesuunta = (tosi_suunta + 180) % 360
                print(f"[KOMPASSI] Näkyvä suunta: {valesuunta:.1f}° | (Todellinen piilotettu)")
            
            # Tila 2: Vääristetty sijainti
            elif tila == 2:
                v_lat = (base_lat + math.sin(sekunnit/100) * 0.1) * 1.618
                v_lon = (base_lon + math.cos(sekunnit/100) * 0.1) / 1.618
                print(f"[SIJAINTI] Vääristetty vektori: {v_lat:.4f}, {v_lon:.4f}")
            
            vaihe += 1
            time.sleep(1) # Vuorottelu sekunnin välein
            
    except KeyboardInterrupt:
        print("\nVuorottelu pysäytetty. Perusta HQ siirtyy pimeään tilaan.")

if __name__ == "__main__":
    perusta_hq_vuorottelu()
