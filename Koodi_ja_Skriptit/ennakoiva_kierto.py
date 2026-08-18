from dna_ydin import hae_ydin, injektoi
import time

class EnnakoivaVayla:
    def __init__(self):
        self.naytot = [" TYHJÄ "] * 7
        # 6 Nanokonetta valmiustilassa (3xTX, 3xRX)
        self.nanokoneet = ["TX1", "TX2", "TX3", "RX1", "RX2", "RX3"]

    def suorita_kierto(self, sana):
        print(f"\n[PÄÄTIETOKONE] Ohjaa 7 näyttöä käyttäen 6 nanokonetta.")
        print(f"[Ennakointi] Käänteinen resurssi ladattu RX-muistiin etukäteen...")
        
        # Generoidaan käänteinen resurssi valmiiksi (ennen kuin viesti saapuu)
        ennakoitu_kaanteinen = sana[::-1]
        
        for sykli in range(7):
            # Lasketaan mikä näyttö lepää (nollapiste) tässä syklissä
            lepo_naytto = sykli
            print(f"\n--- SYKLI {sykli+1} (Lepoasennossa Näyttö {lepo_naytto}) ---")
            
            for n in range(7):
                if n == lepo_naytto:
                    self.naytot[n] = "[SALPA]"
                    print(f" Näyttö {n}: {self.naytot[n]} -> Rele lukittu lepovirtaan.")
                else:
                    # Nanokone tulkkaa ennakoivasti
                    self.naytot[n] = f"DATA:{sana[n % len(sana)]}"
                    print(f" Näyttö {n}: {self.naytot[n]} -> RX nouti valmiin käänteisen: '{ennakoitu_kaanteinen[n % len(sana)]}'")
            
            time.sleep(0.1)

if __name__ == "__main__":
    vayla = EnnakoivaVayla()
    vayla.suorita_kierto("PERUSTA")
