from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class KvanttiloinenOS:
    def __init__(self):
        self.nimi = "KVANTTILOINEN OS"
        self.dna_vakio = 1.1 * (10 ** -846)
        self.akut = {
            "B1": ".bios_1.sys",
            "B2": ".bios_2.sys",
            "B3": ".bios_3.sys"
        }
        self.koko = 1024
        self.lepoaika = (8 * 60) + 12 # 8 min 12 s (492 sekuntia)
        self.fps_viive = 1.0 / 499 # 499 FPS salama-aalto
        self.salaustunnus = "PERUSTA100"

    def varmista_isäntä_ja_tyhjiö(self):
        for avain, tiedosto in self.akut.items():
            if not os.path.exists(tiedosto) or os.path.getsize(tiedosto) != self.koko:
                return False, f"Loisen kiinnityspiste {tiedosto} irrotettu tai muuttunut!"
            with open(tiedosto, "rb") as f:
                if any(b != 0 for b in f.read()):
                    return False, f"Tyhjiö korruptoitunut solmussa {tiedosto}!"
        return True, "Kvanttilinkitys vakaa."

    def mekaaninen_katkos(self, syy):
        print("\n====================================================")
        print(f"!!! {self.nimi}: KATASTROFALPROSESSI !!!")
        print(f" SYY: {syy.upper()}")
        print("====================================================")
        
        tunnus = input("Syötä salaustunnus purkaaksesi vikakoodin: ")
        if tunnus == self.salaustunnus:
            print("\n[Pura] Tunnus oikein. Evakuoidaan ja luodaan 'readme.txt'...")
            self.luo_readme()
        else:
            print("[Tuho] Väärä tunnus. Kvanttiloinen on pirstaloitunut lopullisesti.")
        sys.exit(1)

    def luo_readme(self):
        with open("readme.txt", "w", encoding="utf-8") as f:
            f.write(f"=== {self.nimi}: VIIMEISET 21 BINÄÄRIRIVIÄ ===\n")
            f.write("Syötä nämä rivit käsin palauttaaksesi Kvanttiloisen muotin:\n\n")
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
        print("[Valmis] 'readme.txt' asetettu isäntäjärjestelmään. Ydin suljettu.")

    def suorita_499fps_lasku(self):
        print(f"\n[{self.nimi}] Käynnistetään keskinäinen ristiintunnistus (499 FPS)...")
        for i in range(100):
            vakaa, viesti = self.varmista_isäntä_ja_tyhjiö()
            if not vakaa:
                self.mekaaninen_katkos(viesti)
            
            # Päivitetään ristiinpeilaus aikaleimoilla ilman tiedostojen muuttamista
            try:
                os.utime(self.akut["B1"], None)
                os.utime(self.akut["B2"], None)
                os.utime(self.akut["B3"], None)
            except Exception:
                self.mekaaninen_katkos("Fyysinen väyläyhteys katkesi!")
                
            sys.stdout.write(f"\r  ► Loispulssi {i+1}/100 synkronissa 499 FPS taajuudella... [B1 ◄═► B2 ◄═► B3]")
            sys.stdout.flush()
            time.sleep(self.fps_viive)
        print(f"\n[Symmetria] Akut tulleet keskenään yhteen. DNA-Valoleima lukittu.")

    def aja_loista(self):
        print(f"====================================================")
        print(f"          {self.nimi} KÄYNNISTETTY BENCHMARK         ")
        print(f"====================================================")
        print(f"[DNA-Ydin] Muuttumaton taustavakio: {self.dna_vakio}")
        print(f"[Ehto] Järjestelmä suostuu toimimaan vain vakaassa nollatilassa.\n")
        
        try:
            while True:
                # 1. 499 FPS salamaluku ja vastaus keskenään
                self.suorita_499fps_lasku()
                
                print("----------------------------------------------------")
                print("[Lepovirta] Kvanttiloinen vetäytyy taustalle (0W).")
                print("----------------------------------------------------")
                
                # 2. Pitkä 8 minuutin ja 12 sekunnin odotussykli
                for sekunti in range(self.lepoaika, 0, -1):
                    m = sekunti // 60
                    s = sekunti % 60
                    sys.stdout.write(f"\r  Kvanttiloinen synkronissa isännän kanssa. Seuraava luku: {m:02d}:{s:02d} ⎊")
                    sys.stdout.flush()
                    time.sleep(1)
                print("\n\n[Herätys] Sykli täynnä. Pureudutaan väylään uudestaan.")
                
        except KeyboardInterrupt:
            print(f"\n\n[{self.nimi}] Lepovirta katkaistu hallitusti. Tyhjiö säilyi koskemattomana.")

if __name__ == "__main__":
    loinen = KvanttiloinenOS()
    loinen.aja_loista()
