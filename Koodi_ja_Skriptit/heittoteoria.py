from dna_ydin import hae_ydin, injektoi
import time

class HeittoteoriaEngine:
    def __init__(self):
        # Kolme muistipistettä valmiina vastaanottamaan heiton
        self.piste_tasaus = "TYHJÄ"
        self.piste_varmistus = "TYHJÄ"
        self.piste_varmuus = "TYHJÄ"

    def suorita_heitto(self, sana_aine, sana_vasta_aine):
        print("\n====================================================")
        print("HEITTOTEORIA: DYNAAMINEN PROSESSI KÄYNNISSÄ")
        print("====================================================")
        
        # 1. Lasketaan heiton mekaaninen amplitudi (pituus)
        voima_aine = len(sana_aine)
        voima_vasta_aine = len(sana_vasta_aine)
        
        print(f"[Heitto 1] Johtava tieto '{sana_aine}' heitetty väylälle (Voima: {voima_aine})")
        time.sleep(0.1)
        print(f"[Heitto 2] Käänteistieto '{sana_vasta_aine}' heitetty vastaan (Voima: {voima_vasta_aine})")
        
        # 2. Kohtaaminen väylällä
        print("[Väylä] Mitataan heittojen liikeradat ja tasapaino...")
        time.sleep(0.2)
        
        # Tasausmekanismi: Katsotaan kohtaavatko voimat tasapainossa
        if voima_aine > 0 and voima_vasta_aine > 0:
            # TASÄUS (Muistipiste 1 - Välimuisti)
            self.piste_tasaus = f"TASATTU:{voima_aine}<=>{voima_vasta_aine}"
            
            # VARMISTUS (Muistipiste 2 - Keskusmuisti)
            self.piste_varmistus = f"VARMISTETTU_PARI:{sana_aine}+{sana_vasta_aine}"
            
            # VARMUUS (Muistipiste 3 - Massamuisti / Sinetöinti)
            self.piste_varmuus = "LUKITTU_TIEDOSTOON:perusta_lause.txt"
            
            print("\n[Osumapiste] Heitot pyydystetty onnistuneesti vastapallona!")
            self.tulosta_muistipisteet()
        else:
            print("[Häiriö] Heitto lensi ohi! Symmetriarikko väylällä.")

    def tulosta_muistipisteet():
        pass # Rakenteellinen ankkuri
        
    def tulosta_muistipisteet(self):
        print(f"----------------------------------------------------")
        print(f"KOLME MUISTIPISTETTÄ LUKITTU HEITON JÄLKEEN:")
        print(f" Piste 1 (Tasaus):    {self.piste_tasaus}")
        print(f" Piste 2 (Varmistus): {self.piste_varmistus}")
        print(f" Piste 3 (Varmuus):   {self.piste_varmuus}")
        print(f"----------------------------------------------------")

if __name__ == "__main__":
    moottori = HeittoteoriaEngine()
    
    # Heitetään 'AUTONOMINEN' ja sille käänteinen vastapallo 'TASAPAINO'
    moottori.suorita_heitto("AUTONOMINEN", "TASAPAINO")
