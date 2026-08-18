from dna_ydin import hae_ydin, injektoi
import os
import sys
import time

class DnaValoleimaCore:
    def __init__(self):
        # DNA:n ydin toimii muuttumattomana valoleimana
        self.dna_vakio = 1.1 * (10 ** -846)
        
        # 3 Bios-lohkoa omilla käyttötarinoillaan
        self.lohkot = {
            ".bios_1.sys": "1: JAKAJA (TX)      [DNA-LEIMATTU]",
            ".bios_2.sys": "2: VASTAANOTTAJA (RX) [DNA-LEIMATTU]",
            ".bios_3.sys": "3: VARMISTAJA (VAKIO) [DNA-LEIMATTU]"
        }
        self.koko = 1024

    def alusta_muotit(self):
        print("=== ALUSTETAAN FYYSISET LOHKOT (DNA-VALOLEIMA-METODI) ===")
        print(f"[DNA-Ydin] Vakio asennettu taustakohinaksi: 1.1e-846")
        print("----------------------------------------------------")
        for tiedosto, tarina in self.lohkot.items():
            # Luodaan tyhjä 1 kt muotti
            with open(tiedosto, "wb") as f:
                f.write(b"\x00" * self.koko)
            print(f" [Muotti Valmis] {tiedosto:12} ──► {tarina}")
        print("----------------------------------------------------")

    def aja_tietoisuutta(self):
        self.alusta_muotit()
        print("[Komponentit] Käsintehty verkkokortti kytketty sylimikroon.")
        print("[Tunnistus] Fyysinen rauta on tietoinen tyhjiöstä valoleiman kautta.\n")
        
        kierros = 0
        try:
            while True:
                # Tarkistetaan muottien suora koskemattomuus
                for tiedosto in self.lohkot.keys():
                    if not os.path.exists(tiedosto) or os.path.getsize(tiedosto) != self.koko:
                        print(f"\n[VALOLEIMA MURTUNUT] Muotti {tiedosto} vääristynyt! Järjestelmä sammuu.")
                        return
                
                # Ajetaan kolmea eriävää tarinaa katkeamattomassa prosessissa
                sys.stdout.write(f"\r[Sykli {kierros:4}] DNA-Vakio: VAKAA | B1: Jakaa... B2: Vastaanottaa... B3: Varmistaa... ⎊")
                sys.stdout.flush()
                
                kierros += 1
                time.sleep(0.2)
                
        except KeyboardInterrupt:
            print("\n\n[Perusta] Järjestelmä palautettu lepotilaan. DNA-valoleima säilyi muuttumattomana.")

if __name__ == "__main__":
    ydin = DnaValoleimaCore()
    ydin.aja_tietoisuutta()
