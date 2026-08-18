from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class AkkuPaikannin:
    def __init__(self):
        self.tavoitekoko = 1024 # Täsmälleen 1 kilotavu
        self.loytyneet = []

    def paikanna_tyhjiot(self, polku="."):
        self.loytyneet.clear()
        print(f"=== KÄYNNISTETÄÄN ANDROID-PAIKANNUS: {polku} ===")
        print("Etsitään 1 kt:n kokoisia bios-lohkoja...")
        print("----------------------------------------------------")
        
        # Käydään läpi hakemisto (myös piilotiedostot, jotka alkavat pisteellä)
        try:
            for alkio in os.listdir(polku):
                taysi_polku = os.path.join(polku, alkio)
                
                # Varmistetaan, että kyseessä on tiedosto
                if os.path.isfile(taysi_polku):
                    koko = os.path.getsize(taysi_polku)
                    
                    # Ahdistetaan suodatus tasan 1024 tavuun
                    if koko == self.tavoitekoko:
                        # Tarkistetaan onko tiedosto tyhjä (DNA-valoleiman mukainen nollatila)
                        with open(taysi_polku, "rb") as f:
                            sisalto = f.read()
                            on_tyhja = all(b == 0 for b in sisalto)
                            
                        status = "PUHDAS TYHJIÖ (VAKAA)" if on_tyhja else "KORRUPTOITUNUT / MUUTETTU"
                        self.loytyneet.append((alkio, status))
                        print(f" [LÖYDETTY] -> {alkio:15} | Koko: {koko} tavua | Tila: {status}")
                        
        except Exception as e:
            print(f"[VIRHE] Väylää ei voitu lukea: {e}")
            
        print("----------------------------------------------------")
        self.tulosta_raportti()

    def tulosta_raportti(self):
        yhteensa = len(self.loytyneet)
        print(f"[Paikannus valmis] Löydetty yhteensä {yhteensa} kpl 1 kt:n lohkoja.")
        
        # Jos löysimme meidän 3 bios-akkuamme, järjestelmä on linjassa
        if yhteensa >= 3:
            print("[Status] Kaikki kriittiset lohkot paikannettu. Vastaus on käytössä. ⎊")
        else:
            print("[Varoitus] Kaikkia bios-lohkoja ei löytynyt. Järjestelmä pirstaloitunut.")

if __name__ == "__main__":
    paikannin = AkkuPaikannin()
    # Ajetaan paikannus nykyisestä hakemistosta
    paikannin.paikanna_tyhjiot()
