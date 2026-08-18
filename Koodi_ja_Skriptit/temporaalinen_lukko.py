from dna_ydin import hae_ydin, injektoi
import time

class TemporaalinenLukko:
    def __init__(self):
        self.vaihe_kesto = 492 # 8 min 12 s
        
    def suorita_sykli(self):
        # Vaihe 1: Suora versio (Kirjoitus)
        print("[TILA: SUORA] Kirjoituskone aktiivinen...")
        time.sleep(self.vaihe_kesto)
        
        # Vaihe 2: Käänteinen versio (Vastaanotto)
        print("[TILA: KÄÄNTEINEN] Vastaanotto avattu, odotetaan resonanssia...")
        time.sleep(self.vaihe_kesto)
        
        # Päivitys
        print("[PÄIVITYS] 16m 24s täynnä. Järjestelmän tila synkronoitu.")

# Tämä lukko estää "hämmennyksen", koska järjestelmä tietää 
# tasan tarkkaan, milloin se saa kirjoittaa ja milloin se on kuuntelutilassa.

