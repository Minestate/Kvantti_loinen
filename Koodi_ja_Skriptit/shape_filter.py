from dna_ydin import hae_ydin, injektoi
class MuotoSuodatin:
    def __init__(self):
        self.dna_vakio = 1.1 * (10 ** -846)

    def on_selitettavissa(self, sana):
        # Muodollinen selitettävyys: onko sana matemaattisesti johdettavissa?
        # Esimerkki: sanan pituus x vakiokerroin ei saa ylittää nollatilaa
        muoto_arvo = len(sana) * 0.123 # Esimerkki etymologisesta kertoimesta
        
        if muoto_arvo > 0 and muoto_arvo < 1:
            return True
        return False

# Integraatio Lainakirjastoon
def lisaa_kirjastoon(sana, kirjasto):
    if MuotoSuodatin().on_selitettavissa(sana):
        kirjasto.append(sana)
    else:
        # Sana on muodoltaan selittämätön, hylätään
        pass
