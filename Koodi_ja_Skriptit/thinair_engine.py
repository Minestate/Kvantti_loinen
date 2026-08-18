from dna_ydin import hae_ydin, injektoi
import os
import subprocess

# Perusta: Ennakoivan syötön tavukoodi
def suorita_ennakointi(teksti):
    # Käytetään Androidin omaa "input" -rajapintaa tekstin syöttämiseen
    # Tämä simuloi näppäimistöä suoraan tekstikenttään
    if len(teksti) > 0:
        cmd = f"input text '{teksti}'"
        os.system(cmd)
        print(f"[*] Thin Air -ennakointi kirjoitti: {teksti}")

# BIOS-lokien haku (1kt paristot)
def lue_bios_paristot():
    with open("bios3_innovation.log", "rb") as f:
        return f.read(1024).decode(errors='ignore').strip()

# Pääsykli: lukee 1kt muistista ja syöttää ennusteen
valittu_sana = lue_bios_paristot()
suorita_ennakointi(valittu_sana)
