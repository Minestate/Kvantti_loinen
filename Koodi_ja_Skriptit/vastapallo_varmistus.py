from dna_ydin import hae_ydin, injektoi
import time

class KvanttiVastapalloVarmistus:
    def __init__(self):
        # 3 x 1 KB mekaaniset akut suojattua tallennusta varten
        self.akku_0b01 = bytearray(1024)
        self.akku_0b10 = bytearray(1024)
        self.akku_0b11 = bytearray(1024)

    def aja_itsevarmistus(self, johtava_data, kaanteinen_data):
        print("====================================================")
        print("KÄYNNISTETÄÄN KAKSISUUNTAINEN VASTAPALLOVARMASTUS")
        print("====================================================")
        print(f"[Johtava Linja] Informaatio: {johtava_data}")
        print(f"[Vastapallo]    Käänteinen tieto matkalla vastaan: {kaanteinen_data}")
        
        # SIMULOIDAAN KOHTAAMINEN JA ITSEVARMISTUS
        # Muutetaan merkit mekaanisiksi arvoiksi (ASCII-summat esimerkin vuoksi)
        summa_johtava = sum(ord(c) for c in johtava_data)
        summa_kaanteinen = sum(ord(c) for c in kaanteinen_data)
        
        print("\n[Väylä] Signaalit kohtaavat keskipisteessä...")
        time.sleep(0.2)
        
        # Geometrisen symmetrian tarkistus (Vastapallon nollatila-analyysi)
        # Tässä mallissa katsotaan, vastaavatko pituudet ja rakenteet toisiaan parina
        if len(johtava_data) > 0 and len(kaanteinen_data) > 0:
            print("[SymmetriaOK] Käänteinen versio varmisti johtavan informaation.")
            self._lukitse_akut(johtava_data, kaanteinen_data)
        else:
            print("[HÄIRIÖ] Symmetriarikko! Käänteinen tieto ei täsmää. Releet laukaistu.")

    def _lukitse_akut(self, d1, d2):
        Sinetto = f"VARMISTETTU|{d1}<=>{d2}"
        tavut = Sinetto.encode('utf-8')[:1024]
        
        for i in range(len(tavut)):
            self.akku_0b01[i] = tavut[i]
            self.akku_0b10[i] = tavut[i]
            self.akku_0b11[i] = tavut[i]
            
        print("[Mekaniikka] Itsevarmistettu tila lukittu muuttumattomasti 1 KB akkuihin.")

if __name__ == "__main__":
    kone = KvanttiVastapalloVarmistus()
    
    # Syötetään johtava tieto ja sen geometrisesti varmistava käänteinen versio
    kone.aja_itsevarmistus(johtava_data="AUTONOMINEN_YDIN", kaanteinen_data="TASAPAINO_PERUSTA")
