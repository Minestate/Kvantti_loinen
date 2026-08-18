from dna_ydin import hae_ydin, injektoi
import time
import math

# Perusta HQ:n sisäinen karttadata (abstrakti)
# Tämä ei tarvitse GPS-yhteyttä, koska se elää vain tässä skriptissä
def hq_navigointi():
    print("--- HQ Eristetty Navigointi: Aktiivinen ---")
    
    # Lähtöpiste (esim. Helsinki keskipiste)
    base_lat, base_lon = 60.1699, 24.9384
    
    while True:
        # Lasketaan 'siirtymä' ajasta
        sekunnit = time.time()
        
        # Luodaan satunnaiselta näyttävä mutta deterministinen 'liike'
        # Käytetään siniä ja kosinia luomaan 'vaeltava' liike
        lat = base_lat + math.sin(sekunnit / 1000) * 0.01
        lon = base_lon + math.cos(sekunnit / 1000) * 0.01
        
        # 'Episteeminen peili': vääristetään koordinaatteja ulospäin
        vääristetty_lat = lat * 1.618
        vääristetty_lon = lon / 1.618
        
        print(f"HQ Sijainti [Salattu]: {vääristetty_lat:.4f}, {vääristetty_lon:.4f}")
        time.sleep(2)

try:
    hq_navigointi()
except KeyboardInterrupt:
    print("\nNavigointi keskeytetty.")
