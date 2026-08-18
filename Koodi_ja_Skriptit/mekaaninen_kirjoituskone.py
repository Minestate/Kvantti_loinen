from dna_ydin import hae_ydin, injektoi
import time

class Kirjoituskone:
    def __init__(self):
        self.sanalaskuri = 0
        self.paperin_raja = 150 # 150 sanaa per paperiarkki
        self.kirjoitusvauhti = 0.5 # 0.5 sekuntia per sana (mekaaninen viive)

    def kirjoita(self, sana):
        if self.sanalaskuri >= self.paperin_raja:
            print("\n--- PAPERIN VAIHTO: NOLLATILAN TYHJENNYS ---")
            self.sanalaskuri = 0
            # Tässä kohtaa tyhjennetään puskuri
        
        # Simuloitu mekaaninen viive
        time.sleep(self.kirjoitusvauhti)
        self.sanalaskuri += 1
        return f"Sana '{sana}' kirjoitettu. Arkkia jäljellä: {self.paperin_raja - self.sanalaskuri}"

# Testiajo
kone = Kirjoituskone()
print(kone.kirjoita("Perusta"))
