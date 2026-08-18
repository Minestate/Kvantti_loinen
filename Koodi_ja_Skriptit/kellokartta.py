from dna_ydin import hae_ydin, injektoi
import time
import math
import subprocess

# --- Konfiguraatio ---
lat_alku, lon_alku = 60.1699, 24.9384  # Helsinki lähtöpiste
nopeus_ms = 1.4  # Kävelynopeus
suunta = 45.0    # Perusta HQ:n todellinen suunta

def päivitä_android_gps(lat, lon):
    # Tämä komento syöttää sijainnin suoraan Androidin GPS-rajapintaan
    # Vaatii: pkg install termux-api
    subprocess.run(['termux-location-set', '--lat', str(lat), '--lon', str(lon)])

def perusta_hq_navigointi():
    lat, lon = lat_alku, lon_alku
    print("--- Perusta HQ:n Navigointikerros Aktivoitu ---")
    
    while True:
        # 1. Lasketaan fysiikka (kävelynopeus)
        metri_asteeksi = 1 / 111000
        lat += (nopeus_ms * math.cos(math.radians(suunta)) * metri_asteeksi)
        lon += (nopeus_ms * math.sin(math.radians(suunta)) * metri_asteeksi)
        
        # 2. Vääristetään koordinaatit (Kultainen leikkaus)
        v_lat, v_lon = lat * 1.618, lon / 1.618
        
        # 3. Iskustetaan tieto Androidin ytimeen
        päivitä_android_gps(v_lat, v_lon)
        
        print(f"Iskostettu: Lat {v_lat:.5f}, Lon {v_lon:.5f}")
        time.sleep(1) # Rytmi sekunnin välein

if __name__ == "__main__":
    perusta_hq_navigointi()
