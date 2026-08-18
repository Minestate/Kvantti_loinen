from dna_ydin import hae_ydin, injektoi
import time

class SeitsemanNaytonKone:
    def __init__(self):
        # Geometrinen sanasto
        self.geometria_sanasto = {
            ('g', 'a'): "AUTONOMINEN",
            ('g', 'd'): "YDIN",
            ('a', 'b'): "PERUSTA",
            ('d', 'e'): "TASAPAINO",
            ('a', 'g'): "TEKOÄLY",
            ('b', 'c'): "RELE",
            ('e', 'f'): "MEKAANINEN"
        }
        # Säilytetään kerran käytetyt sanat (Kertakäyttöisyyden valvonta)
        self.kaytetyt_sanat = set()
        
        # Seitsemän 7-segmenttinäytön fyysiset paikat (0-6)
        self.naytot = [None] * 7
        self.naytto_indeksi = 0
        
        self.segmentti_puskuri = []

    def vastaanota_segmentti(self, segmentti):
        self.segmentti_puskuri.append(segmentti)

    def romahduta_ja_sijoita_naytolle(self):
        avain = tuple(self.segmentti_puskuri)
        sana = self.geometria_sanasto.get(avain, "TYHJÄ")
        self.segmentti_puskuri = [] # Tyhjennetään heti iskun jälkeen

        if sana == "TYHJÄ":
            return

        # SÄÄNTÖ 1: Tarkistetaan onko sana käytetty jo kertaalleen
        if sana in self.kaytetyt_sanat:
            print(f"[Estetty] Sana '{sana}' on jo käytetty kerran! Kvanttitila lukittu.")
            return

        # SÄÄNTÖ 2: Sijoitetaan sana vapaalle näytölle (max 7 näyttöä)
        if self.naytto_indeksi < 7:
            self.naytot[self.naytto_indeksi] = sana
            self.kaytetyt_sanat.add(sana) # Merkitään käytetyksi
            print(f"[Mekaniikka] Romahdutettu: '{sana}' -> Ohjattu NÄYTTÖÖN {self.naytto_indeksi}")
            self.naytto_indeksi += 1
        else:
            print("[Varoitus] Kaikki 7 näyttöä ovat jo täynnä!")

    def tallenna_ja_tulosta_muodostelma(self):
        # Rakennetaan lause näytettävistä paikoista
        lause_elementit = [sana for sana in self.naytot if sana is not None]
        koko_lause = " ".join(lause_elementit)
        
        print(f"\n====================================================")
        print(f"7-SEGMENTTINÄYTÖN MUODOSTELMA VALMIS:")
        for i, n in enumerate(self.naytot):
            tila = n if n else "[ Ei signaalia ]"
            print(f" Nayttö {i}: {tila}")
        print(f"====================================================")
        
        # Kirjoitetaan fyysinen teksti tiedostoon 'perusta_lause.txt'
        with open("perusta_lause.txt", "w", encoding="utf-8") as f:
            f.write(koko_lause)
            
        print("[Perusta] Mekaaninen teksti tallennettu tiedostoon: perusta_lause.txt")

if __name__ == "__main__":
    kone = SeitsemanNaytonKone()
    print("====================================================")
    print("ALUSTETAAN 7-SEGMENTTINÄYTÖN PRIORITEETTI-ENNAKOINTI")
    print("====================================================")

    # 1. Ensimmäinen sana: g -> a (AUTONOMINEN)
    kone.vastaanota_segmentti('g')
    kone.vastaanota_segmentti('a')
    kone.romahduta_ja_sijoita_naytolle()

    # 2. Toinen sana: a -> b (PERUSTA)
    kone.vastaanota_segmentti('a')
    kone.vastaanota_segmentti('b')
    kone.romahduta_ja_sijoita_naytolle()

    # 3. Yritetään syöttää 'AUTONOMINEN' uudelleen (g -> a)
    # Tämän pitäisi estyä kertakäyttöisyyden takia!
    kone.vastaanota_segmentti('g')
    kone.vastaanota_segmentti('a')
    kone.romahduta_ja_sijoita_naytolle()

    # 4. Kolmas sana: g -> d (YDIN)
    kone.vastaanota_segmentti('g')
    kone.vastaanota_segmentti('d')
    kone.romahduta_ja_sijoita_naytolle()

    # Tulostetaan seitsemän näytön muodostelma ja tallennetaan
    kone.tallenna_ja_tulosta_muodostelma()
