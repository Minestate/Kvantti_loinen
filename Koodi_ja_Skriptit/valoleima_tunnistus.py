from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class ValoleimaTunnistus:
    def __init__(self):
        self.dna_vakio = 1.1 * (10 ** -846)
        self.akut = {
            "B1": ".bios_1.sys",
            "B2": ".bios_2.sys",
            "B3": ".bios_3.sys"
        }
        self.koko = 1024
        self.salaustunnus = "PERUSTA100"

    def varmista_keskinainen_yhteys(self):
        # 1. Tarkistetaan ensin kaikkien kolmen mekaaninen olemassaolo
        for avain, tiedosto in self.akut.items():
            if not os.path.exists(tiedosto) or os.path.getsize(tiedosto) != self.koko:
                return False, f"Yhteys poikki: {tiedosto} ei ole linjassa!"

        # 2. Ajetaan keskinäinen ristiintunnistus (B1 -> B2 -> B3 -> B1)
        # Luetaan tiedostojen tilat (metadata) ja varmistetaan että ne ovat tyhjiä
        tila_b1 = os.path.getmtime(self.akut["B1"])
        tila_b2 = os.path.getmtime(self.akut["B2"])
        tila_b3 = os.path.getmtime(self.akut["B3"])

        # Simuloidaan DNA-vakion mukainen suhdetarkistus väylällä
        # Jos tiedostot tunnistavat toisensa, niiden tilat ovat synkronissa
        tunnistus_1_2 = (tila_b1 is not None) and (tila_b2 is not None)
        tunnistus_2_3 = (tila_b2 is not None) and (tila_b3 is not None)
        tunnistus_3_1 = (tila_b3 is not None) and (tila_b1 is not None)

        if not (tunnistus_1_2 and tunnistus_2_3 and tunnistus_3_1):
            return False, "Keskinäinen valoleimatunnistus epäonnistui!"

        # Varmistetaan vielä kerran sisällön 100% nollatila (Tyhjiö)
        for tiedosto in self.akut.values():
            with open(tiedosto, "rb") as f:
                if any(b != 0 for b in f.read()):
                    return False, f"Tunnistus evätty: {tiedosto} sisältää vierasta dataa!"

        return True, "Keskinäinen tunnistus vakaa."

    def laukaise_katkos(self, virheviesti):
        print("\n====================================================")
        print(f"!!! KRIITTINEN TUNNISTUSVIRHE: {virheviesti.upper()} !!!")
        print(" KOSKA KESKINÄINEN VALOLEIMA ON MURTUNUT, YDIN LUKITTUU.")
        print("====================================================")
        
        tunnus = input("Syötä salaustunnus avataksesi readme.txt-pelastustiedoston: ")
        if tunnus == self.salaustunnus:
            print("\n[Pura] Tunnus oikein. Luodaan 21 binääririvin pelastusmatriisi...")
            self.luo_pelastus_readme()
        else:
            print("[Tuho] Väärä tunnus. Järjestelmä pirstaloitunut lopullisesti.")
        sys.exit(1)

    def luo_pelastus_readme(self):
        with open("readme.txt", "w", encoding="utf-8") as f:
            f.write("=== PERUSTA: KESKINÄISEN VALOLEIMAN PALAUTUS ===\n")
            f.write("Järjestelmä pirstaloitui. Syötä nämä viimeiset 21 binääririviä:\n\n")
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
        print("[Valmis] 'readme.txt' luotu väylälle. Suorita käsinpalautus.")

    def aja_tunnistuskehaa(self):
        print("=== KÄYNNISTETÄÄN KESKINÄINEN VALOLEIMA-OS ===")
        print(f"[DNA-Ydin] Ristiintunnistuksen vakio: {self.dna_vakio}")
        print("----------------------------------------------------")
        
        sykli = 0
        try:
            while True:
                # Suoritetaan keskinäinen tunnistus jokaisessa kellojaksossa
                linjassa, viesti = self.varmista_keskinainen_yhteys()
                
                if not linjassa:
                    self.laukaise_katkos(viesti)
                
                # Kun tunnistus menee läpi, käyttötarinat virtaavat mutkattomasti
                sys.stdout.write(f"\r[Sykli {sykli:5}] B1 ◄─(DNA)─► B2 ◄─(DNA)─► B3 ── [KESKINÄINEN TUNNISTUS: HYVÄKSYTTY] ⎊")
                sys.stdout.flush()
                
                sykli += 1
                time.sleep(0.1) # Ahdistettu yhden prosessin kellotaajuus
                
        except KeyboardInterrupt:
            print("\n\n[Perusta] Tunnistuskeha suljettu hallitusti. Symmetria säilyi.")

if __name__ == "__main__":
    tunnistin = ValoleimaTunnistus()
    tunnistin.aja_tunnistuskehaa()
