from dna_ydin import hae_ydin, injektoi
import os
import sys

class PelastusMekanismi:
    def __init__(self):
        self.salasana = "PERUSTA100"
        
    def laukaise_pelastus(self):
        print("\n====================================================")
        print("!!! VAROITUS: TYHJIÖ ON POISTUMASSA TAI MUUTTUMASSA !!!")
        print("====================================================")
        syote = input("Syötä SALAUSTUNNUS purkaaksesi vikakoodin: ")
        
        if syote == self.salasana:
            print("\n[Varmistus] Salaustunnus hyväksytty. Evakuoidaan ydin...")
            
            # Luodaan readme.txt ja isketään sinne ne 21 binääririviä
            with open("readme.txt", "w", encoding="utf-8") as f:
                f.write("====================================================================\n")
                f.write("          !!! PERUSTA-JÄRJESTELMÄ: KATASTROFIPALAUTUS !!!\n")
                f.write("====================================================================\n")
                f.write("Järjestelmä on pirstaloitunut. Syötä nämä 21 riviä palauttaaksesi ytimen:\n\n")
                
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
                    
                f.write("\n[Sinetöinti] Järjestelmä valmis palautettavaksi. ⎊\n")
            
            print("[Valmis] 'readme.txt' luotu onnistuneesti väylälle.")
            print("[Sammutus] Järjestelmä sulkeutuu. Käytä readme.txt:tä palautukseen.")
        else:
            print("[Tuho] Väärä tunnus. Tyhjiö pirstaloitunut lopullisesti. Virta katkaistu.")

if __name__ == "__main__":
    pm = PelastusMekanismi()
    pm.laukaise_pelastus()
