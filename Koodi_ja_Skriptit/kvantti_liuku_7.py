from dna_ydin import hae_ydin, injektoi
import time
import sys

class KvanttiLiukuNaytto:
    def __init__(self):
        # 7 näyttöpaikkaa
        self.naytot = [None] * 7
        # Määritellään segmenttipiirrokset eri tiloille
        self.segmentti_grafiikka = {
            "SUORA": "[_a_b_c_     ]", # Oikea/Yläpainotus
            "KÄÄNTEINEN": "[     _d_e_f_]", # Vasen/Alapainotus
            "MENEVÄ": "[_a_     _g_d_]"  # Keskiputki/Tasapaino
        }

    def simuloi_kanava(self, naytto_id, sana_input):
        print(f"\n--- NÄYTTÖ {naytto_id} : AKTIVOIDAAN 6 PÄÄTIETOKONETTA ---")
        print(f"[Input-Signaali]: '{sana_input}'")
        
        # 3 Lähettävää ja 3 Vastaanottavaa nanokonetta käsittelevät 1:2 liukuman
        print("[Mekaniikka] 3xTX ja 3xRX Nanokoneet synkronoivat väylän...")
        
        # 1:2 Suhteen jakautuminen (Suora -> Käänteinen & Menevä)
        suora = sana_input
        kaanteinen = sana_input[::-1] # Käännetään merkit
        meneva = f"{sana_input[len(sana_input)//2:]}{sana_input[:len(sana_input)//2]}" # Liukusiirto
        
        print(f" ├─► [1] SUORA (Aine):        {suora}       {self.segmentti_grafiikka['SUORA']}")
        print(f" ├─► [2] KÄÄNTEINEN (Vasta):   {kaanteinen}       {self.segmentti_grafiikka['KÄÄNTEINEN']}")
        print(f" └─► [2] MENEVÄ (Tasapaino):   {meneva}       {self.segmentti_grafiikka['MENEVÄ']}")
        
        # Lukitaan näytön tila
        self.naytot[naytto_id] = (suora, kaanteinen, meneva)
        time.sleep(0.15)

    def tulosta_kokonaisuus(self):
        print("\n==========================================================================")
        print("                 7 x 7-SEGMENTTINÄYTÖN 1:2 LIUKUMATILA                    ")
        print("==========================================================================")
        for i, tila in enumerate(self.naytot):
            if tila:
                s, k, m = tila
                print(f" NÄYTTÖ {i} ──► [S: {s:11}] ◄──► [K: {k:11}] ◄──► [M: {m:11}] ──► VAKAA (99%)")
            else:
                print(f" NÄYTTÖ {i} ──► [ TYHJÄ / EI SIGNAALIA ]")
        print("==========================================================================")
        print("[Perusta] Kaikki 21 nanokone-paria ovat sinetöineet tilan 100% varmuuteen.")

if __name__ == "__main__":
    simu = KvanttiLiukuNaytto()
    
    # Syötetään 7 mekaanista sanaa järjestelmään
    sanat = [
        "AUTONOMINEN",
        "YDIN",
        "PERUSTA",
        "TASAPAINO",
        "TEKOÄLY",
        "RELE",
        "MEKAANINEN"
    ]
    
    for idx, sana in enumerate(sanat):
        simu.simuloi_kanava(idx, sana)
        
    simu.tulosta_kokonaisuus()
