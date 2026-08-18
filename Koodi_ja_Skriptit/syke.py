from dna_ydin import hae_ydin, injektoi
import time
import random
import os
import time

def herata_solut():
    print("[SYKE] Käynnistetään solujen aktivointi...")
    while True:
        for file in [f for f in os.listdir('.') if f.startswith("solu_REG_")]:
            # Luetaan solun tila ja "käännetään" sen arvoa (simuloidaan sykettä)
            with open(file, "r+b") as f:
                data = f.read()
                # XOR-operaatio luo dynaamisen muutoksen
                uusi_data = bytes([b ^ 0xFF for b in data])
                f.seek(0)
                f.write(uusi_data)
        time.sleep(0.5) # Puolen sekunnin syke

if __name__ == "__main__":
    herata_solut()
def syke():
    print("[SYKE] Käynnistetään elävä syöttö...")
    while True:
        # Generoidaan tutkielman mukaiset arvot (pimeä energia + anti-materia)
        arvot = [
            str(round(random.uniform(1.0, 9.9), 1)), # Pimeä energia
            str(random.randint(0, 9)),             # Anti-materia-peili
            str(random.randint(0, 9)),             # Zombie-aurinko
            "8", "4", "6", "2"                     # DNA-ytimen vakio
        ]
        
        # Kirjoitetaan suoraan rekisteriin
        with open("rekisteri.txt", "w") as f:
            f.write("|".join(arvot))
        
        time.sleep(1) # Sykkeen taajuus 1s

if __name__ == "__main__":
    syke()
