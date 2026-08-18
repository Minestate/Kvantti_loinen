from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class KvanttiloinenOffline:
    def __init__(self):
        self.nimi = "KVANTTILOINEN OS [OFFLINE-YDIN]"
        self.dna_vakio = 1.1 * (10 ** -846)
        self.akut = {
            "B1": ".bios_1.sys",
            "B2": ".bios_2.sys",
            "B3": ".bios_3.sys"
        }
        self.koko = 1024
        self.lepoaika = (8 * 60) + 12 # Tasan 492 sekuntia
        self.fps_viive = 1.0 / 499    # 499 FPS mekaaninen taajuus
        self.salaustunnus = "PERUSTA100"

    def varmista_paikallinen_tyhjio(self):
        # Tarkistetaan mekaaniset muotit paikallisesta tiedostojärjestelmästä
        for avain, tiedosto in self.akut.items():
            if not os.path.exists(tiedosto) or os.path.getsize(tiedosto) != self.koko:
                return False, f"Lohko {tiedosto} irrotettu fyysisesti väylältä!"
            
            with open(tiedosto, "rb") as f:
                if any(b != 0 for b in f.read()):
                    return False, f"Solmu {tiedosto} ylikirjoitettu ulkoisella kohinalla!"
        return True, "Paikallinen suojamuuri vakaa."

    def offline_salpaus(self, syy):
        print("\n====================================================")
        print(f"!!! {self.nimi}: MEKAANINEN SULKU !!!")
        print(f"SYY: {syy.upper()}")
        print(" JÄRJESTELMÄ ON ERISTETTY JA LUKITTU.")
        print("====================================================")
        
        tunnus = input("Syötä salaustunnus purkaaksesi tilan: ")
        if tunnus == self.salaustunnus:
            print("\n[Pura] Salaustunnus hyväksytty. Luodaan 'readme.txt' isäntämuistiin...")
            self.luo_offline_readme()
        else:
            print("[Tuho] Väärä tunnus. Kvanttiloinen pirstaloitui nollatilaan.")
        sys.exit(1)

    def luo_offline_readme(self):
        with open("readme.txt", "w", encoding="utf-8") as f:
            f.write(f"=== {self.nimi}: VIIMEISET 21 BINÄÄRIRIVIÄ ===\n")
            f.write("Järjestelmä on offline-sulussa. Palauta ydin näillä riveillä:\n\n")
            # 21 binäärisuuntaa
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
        print("[Valmis] 'readme.txt' luotu. Käytä sitä linjaamiseen.")

    def suorita_paikallinen_keskustelu(self):
        print(f"\n[{self.nimi}] Ajetaan 499 FPS ristiintunnistus eristetyssä tilassa...")
        for i in range(100):
            vakaa, viesti = self.varmista_paikallinen_tyhjio()
            if not vakaa:
                self.offline_salpaus(viesti)
            
            # Päivitetään paikalliset aikaleimat osoittamaan olemassaoloa
            try:
                os.utime(self.akut["B1"], None)
                os.utime(self.akut["B2"], None)
                os.utime(self.akut["B3"], None)
            except Exception:
                self.offline_salpaus("Paikallinen I/O-väylä petti!")
                
            sys.stdout.write(f"\r  ► Paikallis-pulssi {i+1}/100 [B1 ◄═(DNA)═► B2 ◄═(DNA)═► B3] VAKAA")
            sys.stdout.flush()
            time.sleep(self.fps_viive)
        print(f"\n[Symmetria] Akut sulautuneet yhteen paikallisessa nollapisteessä.")

    def aja_offline_loista(self):
        print(f"====================================================")
        print(f"       {self.nimi} ── PYÖRII TÄYDELLISESSÄ ERISTYKSESSÄ      ")
        print(f"====================================================")
        print(f"[DNA-Tausta] {self.dna_vakio} | [Status] VERKKORADIOT: POISSA PÄÄLTÄ (AIR-GAP)")
        print(f"----------------------------------------------------\n")
        
        try:
            while True:
                # 1. Suoritetaan 499 FPS eristetty keskustelu
                self.suorita_paikallinen_keskustelu()
                
                print("----------------------------------------------------")
                print("[Eristys] Kvanttiloinen nukahtaa offline-lepovirtaan.")
                print("----------------------------------------------------")
                
                # 2. 8 minuutin ja 12 sekunnin paikallinen odotus
                for sekunti in range(self.lepoaika, 0, -1):
                    m = sekunti // 60
                    s = sekunti % 60
                    sys.stdout.write(f"\r  Offline-tasapaino katkeamaton. Seuraava luku: {m:02d}:{s:02d} ⎊")
                    sys.stdout.flush()
                    time.sleep(1)
                print("\n\n[Herätys] Paikallinen kellosykli täynnä. Luetaan muotit.")
                
        except KeyboardInterrupt:
            print(f"\n\n[{self.nimi}] Offline-virta katkaistu hallitusti. Tyhjiö säilyi.")

if __name__ == "__main__":
    loinen = KvanttiloinenOffline()
    loinen.aja_offline_loista()
