# solu_palautus.py
import os
from dna_ydin import hae_ydin

def palauta_solu(tiedosto):
    with open(tiedosto, "wb") as f:
        # Kirjoitetaan vakio-ydin binäärimuodossa
        f.write(str(hae_ydin()).encode())
        print(f"[RE-INK] Solu {tiedosto} vakioitu.")

# Palautetaan kaikki nollakokoiset solut
for file in [f for f in os.listdir('.') if f.startswith("solu_REG_")]:
    if os.path.getsize(file) == 0:
        palauta_solu(file)
