from dna_ydin import hae_ydin, injektoi
import time
import sys

class YhdenProsessinKeskus:
    def __init__(self):
        self.sana = "PERUSTA"
        self.kaanteinen_resurssi = self.sana[::-1]
        self.kellojakso = 0

    def aja_sykli(self):
        print("====================================================")
        print("  AHDISTETTU YHDEN PROSESSIN KVANTTIYDIN (1 THREAD)  ")
        print("====================================================")
        
        # Yksi katkeamaton silmukka hoitaa koko 7-segmenttisen kehän
        while self.kellojakso < 7:
            # Määritetään aktiivinen piste dynaamisesti kellon mukaan
            naytto_id = self.kellojakso
            
            # 1:2 suhteinen tiedon poiminta ilman odotusta
            suora_char = self.sana[naytto_id]
            kaanteis_char = self.kaanteinen_resurssi[naytto_id]
            meneva_char = self.sana[(naytto_id + 3) % 7]
            
            # Mekaaninen suuntasymboli määritetään lennosta indeksin perusteella
            symboli = "▲" if naytto_id % 2 == 0 else "▼"
            if naytto_id == 3: symboli = "◄►"
            
            # Tulostus suoraan väylälle – yksi prosessi hallitsee koko alustan
            sys.stdout.write(f" NÄYTTÖ {naytto_id} ── [{suora_char}] ◄─► [{kaanteis_char}] ◄─► [{meneva_char}] ── SUUNTA: {symboli} (VAKAA)\n")
            sys.stdout.flush()
            
            self.kellojakso += 1
            time.sleep(0.08) # Mekaaninen iskuaika (Klak)

        print("----------------------------------------------------")
        print("[Sinetöinti] Kolossaalinen laskenta ajettu 1 syklissä.")
        print("[Status] Järjestelmä palautettu lepovirtaan. ⎊")

if __name__ == "__main__":
    keskus = YhdenProsessinKeskus()
    keskus.aja_sykli()
