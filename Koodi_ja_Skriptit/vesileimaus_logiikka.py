from dna_ydin import hae_ydin, injektoi
import os
import time

ALUE_X = "./X"
# Vesileima sisältää nyt aikaleiman ja eheyden
def vesileimaa_ja_tiivista():
    rekisteri_entries = []
    aikaleima = time.strftime("%H:%M:%S")
    
    for tiedosto in os.listdir(ALUE_X):
        polku = os.path.join(ALUE_X, tiedosto)
        if os.path.isfile(polku) and os.path.getsize(polku) == 0:
            vesileima_teksti = f"PERUSTA_EHEYS_21 | TS:{aikaleima}"
            
            with open(polku, "w") as f:
                f.write(vesileima_teksti)
            
            # Lisätään rekisteriin (yhteenveto + aikaleima)
            rekisteri_entries.append(f"{tiedosto}:{aikaleima}")
    
    # 1KB tiivistys: vanhat putoavat pois
    rekisteri_data = "|".join(rekisteri_entries)[-1024:]
    with open("rekisteri.txt", "w") as f:
        f.write(rekisteri_data)
