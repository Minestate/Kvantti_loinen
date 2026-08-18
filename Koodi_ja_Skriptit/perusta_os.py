from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class PerustaKyttis:
    def __init__(self):
        self.akut = [".bios_1.sys", ".bios_2.sys", ".bios_3.sys"]
        self.tavoitekoko = 1024
        self.salaustunnus = "PERUSTA100"

    def tarkista_olemassaolo(self):
        # Käyttöjärjestelmän toiminnan ehdoton perusta: tiedetty olemassaolo
        for akku in self.akut:
            if not os.path.exists(akku):
                return False, f"Komponentti {akku} puuttuu väylältä!"
            if os.path.getsize(akku) != self.tavoitekoko:
                return False, f"Komponentin {akku} mekaaninen massa muuttunut!"
                
            # DNA-valoleiman puhtaus (0x00)
            with open(akku, "rb") as f:
                if any(b != 0 for b in f.read()):
                    return False, f"Komponentti {akku} ylikirjoitettu / korruptoitunut!"
                    
        return True, "Kaikki lohkot linjassa."

    def laukaise_salpaus(self, syy):
        print("\n====================================================")
        print(f"!!! KÄYTTÖJÄRJESTELMÄN LUKITUS: {syy.upper()} !!!")
        print(" JÄRJESTELMÄ EI SUOSTU TOIMIMAAN ILMAN 3 X 1 KT TYHJIÖTÄ.")
        print("====================================================")
        
        tunnus = input("Syötä salaustunnus purkaaksesi tilan: ")
        if tunnus == self.salaustunnus:
            print("\n[Pura] Salaustunnus hyväksytty. Luodaan palautusmajakka 'readme.txt'...")
            self.luo_readme()
        else:
            print("[Tuho] Väärä tunnus. Järjestelmä pirstaloitunut. Virta katkaistu.")
        sys.exit(1)

    def luo_readme(self):
        with open("readme.txt", "w", encoding="utf-8") as f:
            f.write("=== PERUSTA KATASTROFIPALAUTUS ===\n")
            f.write("Käytä näitä 21 binääririviä ytimen palauttamiseen:\n\n")
            rivit = [
                "01) 00000001", "02) 01000101", "03) 01010010", "04) 01010101",
                "05) 01010011", "06) 01010100", "07) 01000001", "08) 00000010",
                "09) 01000001", "10) 01010100", "11) 01010011", "12) 01010101",
                "13) 01010010", "14) 01000101", "15) 00000011", "16) 01001110",
                "17) 01000101", "18) 01001110", "19) 01001001", "20) 01001101",
                "21) 00000111"
            ]
            for r in rivit:
                f.write(f"{r}\n")
        print("[Valmis] 'readme.txt' asetettu työpöydälle. Suorita restauraatio.")

    def kaynnista_os(self):
        # Ensimmäinen mekaaninen portti
        vakaa, viesti = self.tarkista_olemassaolo()
        if not vakaa:
            self.laukaise_salpaus(viesti)
            
        print("=== PERUSTA OS: AUTONOMINEN YDIN KÄYNNISSÄ ===")
        print("[Ehto] 3 x 1 kt tiedostojen olemassaolo tunnistettu ja vahvistettu.")
        print("Järjestelmä suostuu toimimaan. Lepovirta vakaa.\n")
        
        kierros = 0
        try:
            while True:
                # Jatkuva lennon aikana tapahtuva olemassaolotarkistus
                vakaa, viesti = self.tarkista_olemassaolo()
                if not vakaa:
                    print("\n[HÄLYTYS] Olemassaolo murtui lennosta!")
                    self.laukaise_salpaus(viesti)
                
                # Käyttöjärjestelmän kolme päävirtausta rullaavat
                sys.stdout.write(f"\r[OS Sykli {kierros:5}] [B1: Jakaa] ─── [B2: Vastaanottaa] ─── [B3: Varmistaa] ⎊")
                sys.stdout.flush()
                
                kierros += 1
                time.sleep(0.1) # Yhden prosessin maksiminopeus
                
        except KeyboardInterrupt:
            print("\n\n[Perusta] Käyttöjärjestelmä suljettu hallitusti. Olemassaolo säilyi katkeamattomana.")

if __name__ == "__main__":
    os_ydin = PerustaKyttis()
    os_ydin.kaynnista_os()
