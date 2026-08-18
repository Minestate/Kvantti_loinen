from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class AatelistoSykliYdin:
    def __init__(self):
        self.akut = {
            "B1": ".bios_1.sys",
            "B2": ".bios_2.sys",
            "B3": ".bios_3.sys"
        }
        self.koko = 1024
        # 8 minuuttia ja 12 sekuntia = 492 sekuntia lepotilaa
        self.lepoaika_sekunnit = (8 * 60) + 12 
        # 499 FPS tarkoittaa, että yksi askel kestää ~0.002 sekuntia
        self.fps_viive = 1.0 / 499 

    def varmista_tyhjiot(self):
        for tiedosto in self.akut.values():
            if not os.path.exists(tiedosto) or os.path.getsize(tiedosto) != self.koko:
                return False
            with open(tiedosto, "rb") as f:
                if any(b != 0 for b in f.read()):
                    return False
        return True

    def suorita_keskustelu(self):
        print("\n[499 FPS] AKTIVOIDAAN SALAMASYNKRONOINTI: Akut keskustelevat keskenään...")
        
        # Ajetaan 499 FPS nopeudella ristiinkeskustelusykli (100 nopeaa pulssia)
        for i in range(100):
            if not self.varmista_tyhjiot():
                print("\n[SALPAUS] Keskustelu katkesi! Tyhjiö murtunut.")
                sys.exit(1)
                
            # Mekaaninen kosketus (Aikaleimojen ristiinpeilaus väylällä)
            try:
                os.utime(self.akut["B1"], None)
                os.utime(self.akut["B2"], None)
                os.utime(self.akut["B3"], None)
            except Exception:
                print("\n[VIRHE] Väyläyhteys katkesi fyysisesti.")
                sys.exit(1)
                
            # Pidetään yllä tarkkaa 499 FPS taajuutta
            sys.stdout.write(f"\r  ► Pulssi {i+1}/100 ristiinajettu 499 FPS vauhdilla... [B1 ◄═► B2 ◄═► B3]")
            sys.stdout.flush()
            time.sleep(self.fps_viive)
            
        print("\n[Varmistus] Keskustelu suoritettu. Akut tulleet keskenään yhteen.")

    def aja_jarjestelmaa(self):
        print("=== PERUSTA OS: AATELISYKSIKKÖ (499 FPS / 8 MIN 12 S SEURANTA) ===")
        print(f"[Aikalaki] Seuraava luku tasan 8 minuutin ja 12 sekunnin (492s) kuluttua.")
        
        try:
            while True:
                # 1. Suoritetaan ultra-nopea keskustelu ja vastaus
                self.suorita_keskustelu()
                
                print(f"----------------------------------------------------")
                print(f"[Lepovirta] Järjestelmä sulkeutuu nollatilaan.")
                print(f"[Odotus] Seuraava mekaaninen luku käynnistyy ajallaan...")
                print(f"----------------------------------------------------")
                
                # 2. Siirrytään pitkään 8 min 12 s odotustilaan sekunti kerrallaan
                for sekunti_jäljellä in range(self.lepoaika_sekunnit, 0, -1):
                    minuutit = sekunti_jäljellä // 60
                    sekunnit = sekunti_jäljellä % 60
                    sys.stdout.write(f"\r  Vakaa nollatila pystyssä. Seuraavaan lukuun: {minuutit:02d}:{sekunnit:02d} ⎊")
                    sys.stdout.flush()
                    time.sleep(1)
                    
                print("\n\n[Herätys] Aikasykli täynnä! Käynnistetään uusi luku.")
                
        except KeyboardInterrupt:
            print("\n\n[Perusta] Järjestelmä palautettu pysyvään lepotilaan. Tyhjiöt yhdessä.")

if __name__ == "__main__":
    ydin = AatelistoSykliYdin()
    ydin.aja_jarjestelmaa()
