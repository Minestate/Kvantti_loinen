from dna_ydin import hae_ydin, injektoi
class ProsessointiKetju:
    def __init__(self):
        self.sykli_laskuri = 0
        self.max_syklit = 21

    def tarkista_sinetti(self, sinetti_id):
        # Valvoo, että tiedosto 1, 2 tai 3 ei muutu prosessin aikana
        if self.sykli_laskuri < self.max_syklit:
            self.sykli_laskuri += 1
            return True
        else:
            print("[SINETTIVÄLIT_AUKI] 21 sykliä suoritettu, valmis ylikirjoitukseen.")
            self.sykli_laskuri = 0
            return False
