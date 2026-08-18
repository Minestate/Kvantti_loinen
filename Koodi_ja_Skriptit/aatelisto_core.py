from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class AatelistoCore:
    def __init__(self):
        # Kolme piilotiedostoa (1 kt = 1024 tavua)
        self.akut = {
            ".akku_1.bin": "JAKAJA (TX)",
            ".akku_2.bin": "VASTAANOTTAJA (RX)",
            ".akku_3.bin": "VARMISTAJA (VAKIO)"
        }
        self.koko = 1024

    def alusta_tyhjio(self):
        print("=== ALUSTETAAN AATELISTO-YDIN: 3 x 1 KT TYHJIÖT ===")
        for tiedosto, tarina in self.akut.items():
            # Luodaan täysin puhdas 1 kt tiedosto täynnä nollatavuun pohjaa (Sama BIOS)
            with open(tiedosto, "wb") as f:
                f.write(b"\x00" * self.koko)
            print(f" [Luotu] Piilotiedosto: {tiedosto:12} | Tarina: {tarina}")
        print("----------------------------------------------------")

    def tarkista_koskemattomuus(self):
        # Tarkistetaan, että tiedostot ovat edelleen täysin tyhjiä (vain nollatavuja)
        for tiedosto in self.akut.keys():
            if not os.path.exists(tiedosto):
                return False, f"Tiedosto {tiedosto} on hävitetty!"
                
            with open(tiedosto, "rb") as f:
                data = f.read()
                # Jos tiedostossa on yksikin tavu, joka EI ole 0x00, tyhjiö on ylikirjoitettu
                if any(b != 0 for b in data) or len(data) != self.koko:
                    return False, f"Tyhjiö korruptoitunut tiedostossa {tiedosto}!"
        return True, "Vakaa"

    def aja_prosessia(self):
        self.alusta_tyhjio()
        
        print("[Status] Järjestelmä käynnissä yhden prosessin nopeudella.")
        print("[Info] Niin kauan kuin akut ovat tyhjinä, toiminta on mutkatonta.")
        print("Paina CTRL+C pysäyttääksesi vakaassa tilassa.\n")
        
        sykli = 0
        try:
            while True:
                # 1. Tarkistetaan mekaaninen suojasalpaus
                vakaa, viesti = self.tarkista_koskemattomuus()
                
                if not vakaa:
                    print("\n====================================================")
                    print(f"!!! MEKAANINEN SALPAUSLAUKEAMINEN: {viesti.upper()} !!!")
                    print(" JÄRJESTELMÄ SAMMUTETAAN VÄLITTÖMÄSTI TURVALLISUUSSYISTÄ.")
                    print("====================================================")
                    break
                
                # 2. Ajetaan dynaamista käyttötarinaa yhdessä suoritusprosessissa
                lataus_symboli = "◄" if sykli % 2 == 0 else "►"
                sys.stdout.write(f"\r[Sykli {sykli:4}] Akku 1: Jakelu... Akku 2: Vastaanotto... Akku 3: Varmistus... {lataus_symboli} [100% VAKAA]")
                sys.stdout.flush()
                
                sykli += 1
                time.sleep(0.2) # Lepovirran taajuus
                
        except KeyboardInterrupt:
            print("\n\n[Perusta] Järjestelmä suljettu hallitusti käyttäjän toimesta. Tyhjiö säilyi.")

if __name__ == "__main__":
    # Korjattu syntaksi: korvattu kaksoispiste oikeaoppisilla suluilla
    core = AatelistoCore()
    core.aja_prosessia()
