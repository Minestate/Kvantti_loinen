import json
import os

class SuodatinAsema:
    def __init__(self, ledger="ledger.json"):
        self.ledger = ledger
        self.tietokanta = "tietokanta.json"

    def suodata_tuplat(self):
        if not os.path.exists(self.ledger): return
        
        # Luetaan uudet tiedot ja pidetään vain uniikit lauseet
        with open(self.ledger, 'r') as f:
            # Käytetään set() -rakennetta poistamaan välittömästi tuplat
            uudet_tiedot = {json.dumps(line.strip()) for line in f if line.strip()}
        
        if os.path.exists(self.tietokanta):
            with open(self.tietokanta, 'r') as f:
                try:
                    tallennettu = set(json.load(f))
                except:
                    tallennettu = set()
        else:
            tallennettu = set()

        # Yhdistetään ja päivitetään
        tallennettu.update(uudet_tiedot)
        
        with open(self.tietokanta, 'w') as f:
            json.dump(list(tallennettu), f)
            
        # Tyhjennetään ledger
        open(self.ledger, 'w').close()
        print(f"[SUODATIN] Tuplat poistettu. Tietokannan eheys maksimoitu.")

if __name__ == "__main__":
    suodatin = SuodatinAsema()
    suodatin.suodata_tuplat()
