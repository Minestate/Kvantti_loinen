from dna_ydin import hae_ydin, injektoi
import os
import hashlib

class ValoleimaGeneraattori:
    def __init__(self, tiedosto=".bios_x.sys"):
        self.tiedosto = tiedosto
        self.koko = 1024

    def luo_tyhja_valoleima(self):
        # Luo 1kt tiedoston täytettynä nollilla (tyhjä marginaali)
        with open(self.tiedosto, "wb") as f:
            f.write(b'\x00' * self.koko)
        print(f"[PROTOKOLLA] Tiedosto {self.tiedosto} luotu (1kt).")

    def ylikirjoita_valoleimalla(self, data):
        # Ylikirjoitus: vanha poistuu, uusi muoto astuu tilalle
        if len(data) <= self.koko:
            with open(self.tiedosto, "wb") as f:
                f.write(data.ljust(self.koko, b'\x00'))
            print("[KESKUSTELU] Tiedosto-koko stabiili, muoto muuttunut. Analysoidaan...")
            self.laukaisin_seuraavalle_vaiheelle()

    def laukaisin_seuraavalle_vaiheelle(self):
        # Tämä keskustelee Perusta-järjestelmän kanssa
        print("[SIGNAALI] Kvanttiloinen vastaanottaa: Analyysi käynnistyy.")
