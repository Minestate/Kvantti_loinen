from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class BiosSimulaatio:
    def __init__(self):
        # 3 Bios-tiedostoa, sama koko (1024 tavua), eri tarina
        self.tiedostot = {
            ".bios_1.sys": {"tarina": "1: JAKAJA (TX)      ", "merkki": "▲"},
            ".bios_2.sys": {"tarina": "2: VASTAANOTTAJA (RX)", "merkki": "▼"},
            ".bios_3.sys": {"tarina": "3: VARMISTAJA (VAKIO)", "merkki": "⎊"}
        }
        self.koko = 1024

    def luo_pohja(self):
        print("=== ALUSTETAAN BIOS-SIMULAATIO (3 x 1 KT TYHJIÖT) ===")
        for nimi, info in self.tiedostot.items():
            with open(nimi, "wb") as f:
                f.write(b"\x00" * self.koko)
            print(f" [Vakaa] {nimi} -> Iskustettu rooli: {info['tarina']}")
        print("----------------------------------------------------")

    def suorita_testaus(self):
        self.luo_pohja()
        print("KÄYNNISTETÄÄN SIMULAATIOTESTAUS... AKUT VALMIINA VÄYLÄLLÄ.")
        print("Paina CTRL+C lopettaaksesi testin.\n")
        
        kierros = 0
        try:
            while True:
                # Tarkistetaan jokainen BIOS-piste erikseen yhdessä kellojaksossa
                for nimi, info in self.tiedostot.items():
                    # 1. Tarkistetaan mekaaninen pystyssäpysyminen (Koko ja tyhjyys)
                    if not os.path.exists(nimi):
                        print(f"\n[TUHO] {nimi} katosi! Salpaus laukeaa.")
                        return
                        
                    with open(nimi, "rb") as f:
                        sisalto = f.read()
                        if len(sisalto) != self.koko or any(b != 0 for b in sisalto):
                            print(f"\n\n[SALPAUS] !!! BIOS-TYHJIÖ RIStory !!! {nimi} ylikirjoitettu!")
                            print("JÄRJESTELMÄ SAMMUU ENNEN KUIN VIRHE LEVIÄÄ PROSESSIIN.")
                            return
                
                # 2. Pyöritetään käyttötarinaa, jos kaikki 3 ovat tyhjinä
                sys.stdout.write(f"\r[Kierros {kierros:4}] B1: {self.tiedostot['.bios_1.sys']['merkki']} Jakaa | B2: {self.tiedostot['.bios_2.sys']['merkki']} Vastaanottaa | B3: {self.tiedostot['.bios_3.sys']['merkki']} Varmistaa -> MUTKATONTA")
                sys.stdout.flush()
                
                kierros += 1
                time.sleep(0.15) # 1:2 liukuman kellotaajuus
                
        except KeyboardInterrupt:
            print("\n\n[Perusta] Simulaatiotesti keskeytetty vakaassa tilassa. Kaikki bios-akut säilyivät puhtaina.")

if __name__ == "__main__":
    simu = BiosSimulaatio()
    simu.suorita_testaus()
