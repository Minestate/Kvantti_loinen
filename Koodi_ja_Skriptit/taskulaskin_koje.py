from dna_ydin import hae_ydin, injektoi
import time
import sys

class MekaaninenKoje:
    def __init__(self):
        # 7 hammasratasta (näyttöä), aluksi nollatilassa (0)
        self.rattaat = [0] * 7
        # 6 siirtovipua valmiina välittämään muistikymmenet
        self.vivut = 6

    def pyorayta_ratasta (self, paikka, napsautukset):
        print(f"\n[KÄYTTÄJÄ] Pyöräyttää ratasta {paikka} +{napsautukset} hammasta.")
        
        for _ in range(napsautukset):
            self.rattaat[paikka] += 1
            time.sleep(0.05)
            
            # Mekaaninen kymmenen siirto (Ysin yli romahdus nollaan)
            if self.rattaat[paikka] == 10:
                self.rattaat[paikka] = 0
                print(f"  *KLAK* -> Ratas {paikka} saavutti nollapisteen! Aktivoidaan siirtovipu.")
                
                # Siirretään voima seuraavalle rattaalle (jos mahdollista)
                if paikka + 1 < 7:
                    self.rattaat[paikka + 1] += 1
                    print(f"    -> Vipu siirsi +1 hammasta ratkaalle {paikka + 1} *KLIK*")

    def tulosta_naytto(self):
        print("\n====================================================")
        # Piirretään mekaaninen 7-segmenttinäyttö kiekoista
        naytto_str = " ".join([f"[{r}]" for r in reversed(self.rattaat)])
        print(f" MEKAANINEN LASKENTATELA:  {naytto_str}")
        print("====================================================")
        print("[Perusta] Hammasrattaiden asento vakaa. Lepovirta: 0W.")

if __name__ == "__main__":
    koje = MekaaninenKoje()
    
    print("=== PERIAATTEELLINEN MEKAANINEN TASKULASKIN-KOJE ===")
    koje.tulosta_naytto()
    
    # Tehdään ensimmäinen mekaaninen siirto: lisätään ykkösten rattaaseen (paikka 0) 9 hammasta
    koje.pyorayta_ratasta(0, 9)
    koje.tulosta_naytto()
    
    # Pyöräytetään vielä 2 hammasta lisää, jolloin mekaaninen vipu joutuu töihin
    koje.pyorayta_ratasta(0, 2)
    koje.tulosta_naytto()
