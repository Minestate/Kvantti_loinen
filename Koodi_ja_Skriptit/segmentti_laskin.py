from dna_ydin import hae_ydin, injektoi
class SegmenttiLaskin:
    def __init__(self):
        # 7-segmentti-indeksit: kirjain -> tarvittavien segmenttien määrä
        self.segmentti_kartta = {'A': 6, 'B': 5, 'C': 4, 'D': 5, 'E': 5, 'F': 4, 'G': 5, 'H': 4}
        self.max_segmentit = 1024
        self.nykyinen_summa = 0

    def syota_merkki(self, merkki):
        kulutus = self.segmentti_kartta.get(merkki.upper(), 3) # Oletus 3 jos tuntematon
        if self.nykyinen_summa + kulutus > self.max_segmentit:
            return "--- PAPERI TÄYNNÄ: YLIKIRJOITUS ---"
        self.nykyinen_summa += kulutus
        return f"Segmentit: {self.nykyinen_summa}/{self.max_segmentit}"
