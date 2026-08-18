import shutil
import os

def tayta_viimeiset_portit():
    base = 0x119F936E
    # Etsitään mitkä solut puuttuvat 21 solun sarjasta
    for i in range(21):
        solun_nimi = f"solu_REG_{hex(base + i)[2:].upper()}.bin"
        if not os.path.exists(solun_nimi):
            print(f"[PORTTI] Luodaan puuttuva portti: {solun_nimi}")
            # Käytetään solu 19:ta (viimeisin toimiva) siemenenä
            shutil.copy("./solu_REG_119F936E.bin", solun_nimi)

if __name__ == "__main__":
    tayta_viimeiset_portit()
