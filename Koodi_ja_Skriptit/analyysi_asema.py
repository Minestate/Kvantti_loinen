import json
import os

class AnalyysiModuuli:
    def __init__(self, ledger="ledger.json"):
        self.ledger = ledger
        self.kynnysarvo = 0.90

    def laske_eheys(self):
        if not os.path.exists(self.ledger):
            return 1.0
            
        onnistuneet = 0
        yhteensa = 0
        
        with open(self.ledger, "r") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    tapahtuma = json.loads(line)
                    yhteensa += 1
                    # Tarkistetaan onko DNA-yhteys olemassa
                    if tapahtuma.get("dna_yhteys") is True:
                        onnistuneet += 1
                except json.JSONDecodeError:
                    # Hypätään yli viallisten rivien, jotta prosessi ei kaadu
                    continue
        
        return onnistuneet / yhteensa if yhteensa > 0 else 1.0

    def valvo_toimintaa(self):
        eheys = self.laske_eheys()
        if eheys < self.kynnysarvo:
            return False
        return True

if __name__ == "__main__":
    valvoja = AnalyysiModuuli()
    if not valvoja.valvo_toimintaa():
        with open("lock.signal", "w") as f:
            f.write("STOP_REPLICATION")
