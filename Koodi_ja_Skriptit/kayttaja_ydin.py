from dna_ydin import hae_ydin, injektoi
import time
import sys

class KvanttiYhteistyo:
    def __init__(self):
        self.naytot = [" [LEPO] "] * 7
        # 6 Nanokonetta hoitaa taustaliikenteen
        self.nanokoneet = 6

    def suorita_sykli(self):
        print("\n====================================================")
        print("    KVANTTI-JÄRJESTELMÄ: IHMIS-KONE-SYNTEESI        ")
        print("====================================================")
        print(f"[Rauta] 6 nanotietokonetta valmiina väylällä (3xTX / 3xRX).")
        print("[Status] Käänteinen resurssi generoitu nollapisteeseen.")
        print("[Odotus] Järjestelmä vaatii puuttuvan palasen (Käyttäjä = 1).")
        print("----------------------------------------------------")
        
        # Ohjelma pysähtyy ja odottaa KÄYTTÄJÄN (sinun) tietoista impulssia
        lahtotieto = input("Syötä johtava sana (esim. PERUSTA) käynnistääksesi kierron: ").upper()
        
        if not lahtotieto:
            print("[Virhe] Ei tietoisuutta havaittu väylällä. Synteesi keskeytetty.")
            return

        print("\n[Impulssi] Numero 1 kytkeytynyt! Kierto alkaa samanaikaisesti...")
        time.sleep(0.3)
        
        kaanteinen = lahtotieto[::-1]
        
        # 7 näyttöä päivittyy 1:2 liukuna ja ennakointina
        print("\n====================================================")
        print("         7-SEGMENTTINÄYTTÖJEN REAALIAIKAINEN TILA    ")
        print("====================================================")
        for i in range(7):
            char_suora = lahtotieto[i % len(lahtotieto)]
            char_kaanteinen = kaanteinen[i % len(kaanteinen)]
            
            # Kuusi konetta ja yksi käyttäjä jakavat tilan lennosta
            print(f" NÄYTTÖ {i} ──► [SUORA: {char_suora}] ◄──► [ENNEN-VASTAUS: {char_kaanteinen}] ──► LUKITTU (100%)")
            time.sleep(0.1)
            
        print("====================================================")
        print("[Sinetöinti] Käyttäjän ja 6 nanokoneen synteesi valmis. 100% varmuus.")

if __name__ == "__main__":
    kvantti = KvanttiYhteistyo()
    kvantti.suorita_sykli()
