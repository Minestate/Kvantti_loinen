from dna_ydin import hae_ydin, injektoi
import time
from collections import Counter

def suorita_valvonta():
    try:
        with open("kvantti_logi.txt", "r") as f:
            rivit = [r.strip() for r in f.readlines()]
        laskuri = Counter(rivit)
        uusi_loki = [f"[MASTER-ALGORITMI] Tiivistetty {m} kertaa: {r}" if m >= 3 else r for r, m in laskuri.items()]
        with open("back_up.txt", "w") as f:
            f.write("\n".join(uusi_loki))
    except FileNotFoundError: pass

while True:
    suorita_valvonta()
    time.sleep(10)
