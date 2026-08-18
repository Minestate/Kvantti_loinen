import json
import time
import os
from core_dna import DNA_CORE, valtuuta_prosessi

def yhdistä_tilat():
    # Komponenttien tuottamat väliaikaiset tilat
    komponentit = ["redball_state.json", "valo_kenno_state.json", "kello_state.json"]
    kokonais_status = {}

    for tiedosto in komponentit:
        if os.path.exists(tiedosto):
            try:
                with open(tiedosto, "r") as f:
                    kokonais_status.update(json.load(f))
            except:
                continue
    
    # Kirjoitetaan yhdistetty status selainta varten
    with open("perusta_status.json", "w") as f:
        json.dump(kokonais_status, f)

def pyöritä_asemaa():
    if not valtuuta_prosessi(DNA_CORE):
        print("DNA-yhteys evätty.")
        return

    print("--- Logiikka-asema aktivoitu: Keskittää datavirrat ---")
    try:
        while True:
            yhdistä_tilat()
            time.sleep(0.5) # Päivitystiheys
    except KeyboardInterrupt:
        print("Logiikka-asema pysäytetty.")

if __name__ == "__main__":
    pyöritä_asemaa()
