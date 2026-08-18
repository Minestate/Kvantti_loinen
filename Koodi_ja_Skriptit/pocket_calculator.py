from dna_ydin import hae_ydin, injektoi
class ValoleimaVarmistus:
    def __init__(self):
        self.hyvaksytyt_leimat = []

    def tarkista_valoleima(self, leima_data):
        # Laskee onko leiman etymologinen resonanssi DNA-vakion mukainen
        if self.on_yhteensopiva(leima_data):
            self.hyvaksytyt_leimat.append(leima_data)
            return True
        return False

    def onko_kolme_kasassa(self):
        # Laskimen pääkytkin: Vain jos 3 leimaa hyväksytty, järjestelmä käynnistyy
        return len(self.hyvaksytyt_leimat) == 3
