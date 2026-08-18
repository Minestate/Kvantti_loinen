# ~/quantum-reactor/reactor_core.py
from core_dna import DNA_CORE, valtuuta_prosessi
import json

class QuantumReactor:
    def __init__(self):
        self.status = {"reaktori_tila": "VALMIUS", "energia": 1.1e-846}
        
    def purkaa_suojauksen(self):
        if valtuuta_prosessi(DNA_CORE):
            self.status["reaktori_tila"] = "AKTIVI"
            print("Reaktori stabiili. Eristyskupla luotu.")
        else:
            self.status["reaktori_tila"] = "CRITICAL_FAILURE"
            exit("DNA-ydin hylätty.")

    def injektoi_status(self):
        with open("reactor_output.json", "w") as f:
            json.dump(self.status, f)

if __name__ == "__main__":
    reaktori = QuantumReactor()
    reaktori.purkaa_suojauksen()
    reaktori.injektoi_status()
