from dna_ydin import hae_ydin, injektoi
import time

class HajautettuMekaaninenMuisti:
    def __init__(self):
        # Kolme hajautettua 1 KB:n akkua
        self.lohko_reaali = bytearray(1024)      # Aine
        self.lohko_heijastus = bytearray(1024)   # Vasta-aine
        self.lohko_tasapaino = bytearray(1024)   # Sinetöinti / Status
        
    def hajauta_tieto(self, naytto_id, sana, segmentit):
        print(f"\n--- ALUSTETAAN HAJAUTETTU MUISTIOPERAATIO (Näyttö {naytto_id}) ---")
        print(f"[Input] Sana: '{sana}' | Aktiiviset segmentit: {segmentit}")
        
        # 1. Hajautetaan reaaliosa (Sana ja paikka)
        data_reaali = f"NAYTTO:{naytto_id}|SANA:{sana}"
        tavut_reaali = data_reaali.encode('utf-8')[:1024]
        for i in range(len(tavut_reaali)):
            self.lohko_reaali[i] = tavut_reaali[i]
            
        # 2. Hajautetaan heijastusosa (Segmenttilogiikka)
        data_heijastus = f"SEGMENTIT:{''.join(segmentit)}"
        tavut_heijastus = data_heijastus.encode('utf-8')[:1024]
        for i in range(len(tavut_heijastus)):
            self.lohko_heijastus[i] = tavut_heijastus[i]
            
        # 3. Hajautetaan vakaustila (Akkujen varmistussalpa)
        data_tasapaino = "STATUS:VAKAA_NOLLATILA|RELEET:LUKITTU"
        tavut_tasapaino = data_tasapaino.encode('utf-8')[:1024]
        for i in range(len(tavut_tasapaino)):
            self.lohko_tasapaino[i] = tavut_tasapaino[i]
            
        print("[Mekaniikka] Tieto pilkottu ja hajautettu onnistuneesti kolmeen lohkoon.")
        self.nayta_hajautettu_tila()

    def nayta_hajautettu_tila(self):
        print(f" -> Lohko 1 (Reaali) sisältö:   {self.lohko_reaali.decode('utf-8').strip(chr(0))}")
        print(f" -> Lohko 2 (Heijastus) sisältö: {self.lohko_heijastus.decode('utf-8').strip(chr(0))}")
        print(f" -> Lohko 3 (Tasapaino) sisältö: {self.lohko_tasapaino.decode('utf-8').strip(chr(0))}")

if __name__ == "__main__":
    muisti = HajautettuMekaaninenMuisti()
    
    # Hajautetaan ensimmäisen näytön tiedot ('AUTONOMINEN', segmentit 'g' ja 'a')
    muisti.hajauta_tieto(naytto_id=0, sana="AUTONOMINEN", segmentit=['g', 'a'])
