class ArvoAvaruusYksikko:
    def __init__(self, arvo, yksikko):
        self.arvo = arvo
        self.yksikko = yksikko

    def __mul__(self, other):
        """Kertolasku ja yksiköiden yhdistäminen"""
        uusi_arvo = self.arvo * other.arvo
        uusi_yksikko = f"({self.yksikko} * {other.yksikko})"
        return ArvoAvaruusYksikko(uusi_arvo, uusi_yksikko)

    def __truediv__(self, other):
        """Jakolasku ja yksiköiden supistaminen/jakaminen"""
        uusi_arvo = self.arvo / other.arvo
        uusi_yksikko = f"({self.yksikko} / {other.yksikko})"
        return ArvoAvaruusYksikko(uusi_arvo, uusi_yksikko)

    def nayta_tila(self):
        """Näyttää suuruusluokan ja yksikön paljastamatta suoraan tarkkaa loppusummaa"""
        import math
        if self.arvo == 0:
            pituus = 0
        else:
            pituus = int(math.log10(abs(self.arvo))) + 1
        
        print(f"Suuruusluokka: {pituus} numeroa pitkä luku")
        print(f"Matemaattinen yksikkö: {self.yksikko}")
        print("-" * 40)

# --- JÄRJESTELMÄN SUORITUSKAAVIO ---

# Askel 1: Alkuperäinen eurojen kohtaaminen (14 446.66 € * 200 000 €)
pohja_a = ArvoAvaruusYksikko(14446.66, "€")
pohja_b = ArvoAvaruusYksikko(200000, "€")
neliö_eurot = pohja_a * pohja_b

print("Vaihe 1: Euron neliöiden synnyttäminen")
neliö_eurot.nayta_tila()

# Askel 2: Jakaminen suhteellisella europrosentilla (0.05 €%)
# Jakaminen muuttaa euron neliöt takaisin kappaleiksi (20-kertaistaa arvon numerotason)
jakaja_prosentti = ArvoAvaruusYksikko(0.05, "€%")
kolikko_kappaleet = neliö_eurot / jakaja_prosentti

print("Vaihe 2: Suhteellisen europrosentin (€%) kohtaaminen")
kolikko_kappaleet.nayta_tila()

# Askel 3: Kolikkojen muuttaminen takaisin lineaariseksi euroarvoksi
# Koska kyseessä on 5 sentin kolikot, jaetaan kappaleet suhteella 20 (tai kerrotaan 0.05)
viisi_senttiä = ArvoAvaruusYksikko(20, "kpl/€")
lineaariset_eurot = kolikko_kappaleet / viisi_senttiä

print("Vaihe 3: Paluu lineaariseksi euroarvoksi (Kolikoiden niputus)")
lineaariset_eurot.nayta_tila()

# Askel 4: Viimeisin siirto dynaamiseen arvotiheyteen (kerrotaan 0.05 €²/kk²)
arvo_tiheys = ArvoAvaruusYksikko(0.05, "€²/kk²")
kuutio_ulottuvuus = lineaariset_eurot * arvo_tiheys

print("Vaihe 4: Kolmiulotteinen laajentuminen (Massa neliökilometreillä)")
kuutio_ulottuvuus.nayta_tila()