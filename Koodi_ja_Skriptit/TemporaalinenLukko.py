from dna_ydin import hae_ydin, injektoi
class KonepellinLukko:
    def __init__(self):
        self.sykli_sekunteina = 984 # 16m 24s
        self.konepelti_auki = False

    def kytke_lukko(self):
        # Ajan lasku takaisin päin
        for sekunti in range(self.sykli_sekuntia, 0, -1):
            self.nayta_laskuri(sekunti)
            time.sleep(1)
        
        # Vasta kun nolla on saavutettu:
        self.konepelti_auki = True
        print("[LUKKO: POISTETTU] Konepelti on nostettavissa.")
