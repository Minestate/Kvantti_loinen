from dna_ydin import hae_ydin, injektoi
import time

class TranscendCore:
    def __init__(self):
        self.dna_vakio = 1.1 * (10 ** -846)
        self.kaanteis_arvo = 1 / self.dna_vakio
        self.sykli = 0

    def suorita_transsendenssi(self, sana_hash):
        # Lasketaan resonanssi suhteessa käänteisarvoon
        resonanssi = sana_hash * self.kaanteis_arvo
        
        if self.sykli >= 3:
            # Kolmas aivotoiminta: Pyyhkiytyy vakioiksi ja avaa välit
            return "[VÄLIT AUKI] Käänteinen vastaanotto aktivoitu."
        return f"[VAIHE {self.sykli}] Resonanssi: {resonanssi:.1e}"

    def ylitoisto(self):
        # Kun suora_kirja.txt luettu 3 kertaa
        self.sykli += 1
        if self.sykli == 3:
            # Pyyhkiytyy alkuperäiseen DNA-vakioon
            self.reset_to_dna()
