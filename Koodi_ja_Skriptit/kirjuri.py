from dna_ydin import hae_ydin, injektoi
import os

def paivita_rekisteri(uusi_summaus):
    REKISTERI = "rekisteri.txt"
    MAX_SIZE = 1024 # 1 KB

    # Luetaan nykyinen rekisteri
    sisalto = ""
    if os.path.exists(REKISTERI):
        with open(REKISTERI, "r") as f:
            sisalto = f.read()

    # Lisätään uusi summaus loppuun
    uusi_sisalto = (sisalto + "\n" + uusi_summaus)[-MAX_SIZE:]

    # Tallennetaan takaisin
    with open(REKISTERI, "w") as f:
        f.write(uusi_sisalto)
