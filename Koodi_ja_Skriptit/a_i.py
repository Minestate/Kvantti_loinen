from dna_ydin import hae_ydin, injektoi
import random
import re
import time

class EnnustavaTekoaly:
    def __init__(self):
        # Aiempi kiinteä tietopohja
        self.tietopohja = {
            "tutkimus": ["Tutkielman tila on dokumentoitu ja suljettu myöhempää tarkastelua varten."],
            "status": ["Kaikki offline-järjestelmät toimivat optimaalisesti."]
        }
        
        # Dynaaminen muisti ennakoivaa tekstinsyöttöä varten (Markov-ketju)
        # Rakenne: { "sana": { "seuraava_sana": kerrat } }
        self.ennustus_muisti = {}
        
        # Opetetaan järjestelmälle heti alussa sen omat perustiedot, jotta sillä on pohja mistä ennustaa
        self._esiopeta_muisti()

    def _puhdista_ja_pilko(self, teksti):
        """Puhdistaa tekstin ja palauttaa sen sanalistana."""
        teksti = teksti.lower()
        teksti = re.sub(r'[^\w\s]', '', teksti)
        return teksti.split()

    def opi_lause(self, lause):
        """Pilkkoo lauseen ja tallentaa sanojen väliset siirtymät muistiin."""
        sanat = self._puhdista_ja_pilko(lause)
        if len(sanat) < 2:
            return

        for i in range(len(sanat) - 1):
            nykyinen = sanat[i]
            seuraava = sanat[i+1]
            
            if nykyinen not in self.ennustus_muisti:
                self.ennustus_muisti[nykyinen] = {}
            
            if seuraava not in self.ennustus_muisti[nykyinen]:
                self.ennustus_muisti[nykyinen][seuraava] = 0
                
            self.ennustus_muisti[nykyinen][seuraava] += 1

    def _esiopeta_muisti(self):
        """Syöttää järjestelmän omat lauseet muistiin ennustepohjaksi."""
        lauseet = [
            "tutkielman tila on dokumentoitu ja suljettu myöhempää tarkastelua varten",
            "perusta base on määritetty järjestelmän pysyväksi ankkuriksi",
            "kaikki tiedot on vakuutettu ja säilötty muistiin talteen"
        ]
        for l in lauseet:
            self.opi_lause(l)

    def ennusta_seuraava_sana(self, nykyinen_teksti):
        """Katsoo viimeistä kirjoitettua sanaa ja ehdottaa siihen sopivaa jatkoa."""
        sanat = self._puhdista_ja_pilko(nykyinen_teksti)
        if not sanat:
            return None
            
        viimeisin_sana = sanat[-1]
        
        if viimeisin_sana in self.ennustus_muisti:
            vaihtoehdot = self.ennustus_muisti[viimeisin_sana]
            # Valitaan suosituin/todennäköisin seuraava sana
            paras_jatko = max(vaihtoehdot, key=vaihtoehdot.get)
            return paras_jatko
        return None

# --- Järjestelmän demonstrointi ---
if __name__ == "__main__":
    äly = EnnustavaTekoaly()
    print("=== ENNAKOIVA OFF-LINE MOOTTORI AKTIVOITU ===")
    print("Kirjoita lauseen alku (esim. 'tutkielman tila') nähdäksesi ennustuksen.\n")
    
    # Simuloidaan tilannetta, jossa käyttäjä alkaa kirjoittaa
    testisyotteet = ["tutkielman", "tutkielman tila", "kaikki tiedot"]
    
    for syote in testisyotteet:
        print(f"Kirjoitat parhaillaan: '{syote}...'")
        ennustus = äly.ennusta_seuraava_sana(syote)
        if ennustus:
            print(f"-> Tekoälyn ennustus seuraavaksi sanaksi: [ {ennustus} ]")
        else:
            print("-> Ei ennustetta saatavilla tästä sanasta.")
        print("-" * 40)
        time.sleep(0.5)
