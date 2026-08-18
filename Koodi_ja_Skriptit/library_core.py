from dna_ydin import hae_ydin, injektoi
import os

class Lainakirjasto:
    def __init__(self, tiedosto):
        self.tiedosto = tiedosto
        self.lainatut_sanat = self._lataa_kirjasto()

    def _lataa_kirjasto(self):
        # Lainaamme sanat muistiin, emme muokkaa alkuperäistä
        with open(self.tiedosto, "r") as f:
            return f.read().split()

    def hae_sana(self, indeksi):
        # Palauttaa sanan, kunnes "muut sanaparit" siirtävät sen
        return self.lainatut_sanat[indeksi % len(self.lainatut_sanat)]

    def siirra_olopaikka(self, uudet_sanaparit):
        # Kun uudet parit saapuvat, lainakirjasto päivittyy
        self.lainatut_sanat = uudet_sanaparit
        print("[LAINAKIRJASTO] Olopaikka päivitetty.")
