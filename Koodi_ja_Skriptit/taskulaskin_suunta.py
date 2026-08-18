from dna_ydin import hae_ydin, injektoi
import time
import sys

class SuuntaavaLaskin:
    def __init__(self):
        # 7 mekaanista numerorattaispaikkaa
        self.rattaat = [0] * 7
        self.romahdukset = 0 # Seuraa nollapisteiden kohtaamista

    def pyorayta_laskentaa(self, paikka, hammastukset):
        print(f"\n[KÄYTTÄJÄ] Impulssi paikkaan {paikka}: +{hammastukset} hammasta.")
        
        for _ in range(hammastukset):
            self.rattaat[paikka] += 1
            time.sleep(0.02)
            
            if self.rattaat[paikka] == 10:
                self.rattaat[paikka] = 0
                self.romahdukset += 1 # Mekaaninen kierto saavutti nollan
                if paikka + 1 < 7:
                    self.rattaat[paikka + 1] += 1

    def maarita_suuntasymboli(self, viimeisin_lisays):
        # Lasketaan kaavan suunta suhteessa romahdusten ja lisäysten määrään
        if self.romahdukset == 0:
            return "▲ [SUORA VIRTAUS]"
        elif self.romahdukset % 2 == 0 and viimeisin_lisays > 0:
            return "◄► [LIUKUVA TASAPAINO]"
        elif self.romahdukset > 0 and viimeisin_lisays % 2 == 0:
            return "▼ [KÄÄNTEINEN VASTAPALLO]"
        else:
            return "⎊ [SINETÖITY NOLLATILA]"

    def tulosta_lopputeema(self, viimeisin_lisays):
        naytto_str = " ".join([f"[{r}]" for r in reversed(self.rattaat)])
        symboli = self.maarita_suuntasymboli(viimeisin_lisays)
        
        print("\n====================================================")
        print(f" MEKAANINEN TELA: {naytto_str}")
        print(f" LASKUKAAVAN SUUNTA: {symboli}")
        print("====================================================")
        print("[Perusta] Tulos ja suuntasymboli lukittu muistiin.")

if __name__ == "__main__":
    koje = SuuntaavaLaskin()
    
    print("=== SUUNTAAVAN TASKULASKIMEN PERUSTA ===")
    
    # Esimerkki 1: Suora lisäys ilman romahdusta
    koje.pyorayta_laskentaa(0, 5)
    koje.tulosta_lopputeema(5)
    
    # Esimerkki 2: Lisäys, joka ajaa rattaan nollapisteen yli (Vastapallo aktivoituu)
    koje.pyorayta_laskentaa(0, 6)
    koje.tulosta_lopputeema(6)
