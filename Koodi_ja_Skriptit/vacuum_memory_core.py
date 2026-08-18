from dna_ydin import hae_ydin, injektoi
import os

class VacuumMemory:
    def __init__(self, tiedosto=".bios_1.sys"):
        self.tiedosto = tiedosto
        self.koko = 1024 # 1kt

    def suodata_ja_paivita(self, uusi_sana):
        # 1. Lue nykyinen 1kt tila
        with open(self.tiedosto, "rb") as f:
            data = bytearray(f.read(self.koko))

        # 2. Suodata: Jos sana ei ole "selitettävissä", hylätään
        if not self.on_selitettavissa(uusi_sana):
            return # Vanha pysyy, uusi hylätään

        # 3. Tyhjän marginaalin luonti (Siirtymä):
        # Ylivuoto (vanhin data) siirretään pois ja uusi kirjoitetaan tilalle
        uusi_tavu = self.trinity_encode(uusi_sana)
        data = data[1:] + bytes([uusi_tavu]) 

        # 4. Kirjoitus: Vanha on mennyt, uusi on nyt nollatilassa
        with open(self.tiedosto, "wb") as f:
            f.write(data)

    def on_selitettavissa(self, sana):
        # "Muoto-suodatin": vain vakaat muodot hyväksytään
        return len(sana) > 0 and len(sana) < 16
