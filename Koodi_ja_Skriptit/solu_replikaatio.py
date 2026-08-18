import shutil
import os

def replikoi_solut():
    olemassa_olevat = [
        "./solu_REG_119F936E.bin", 
        "./solu_REG_1283A5E9.bin", 
        "./solu_REG_12E1F215.bin"
    ]
    
    print("[REPLIKAATIO] Täytetään puuttuvat 18 solua...")
    
    # Käytetään olemassa olevia soluja "siemeninä" uusille soluille
    for i in range(18):
        # Luodaan uusi osoite (simuloitu lineaarisesti)
        uusi_hex = hex(0x119F936E + i + 1).replace('0x', '').upper()
        uusi_nimi = f"./solu_REG_{uusi_hex}.bin"
        
        # Kopioidaan siemen (valitaan 1. solu siemeneksi)
        shutil.copy(olemassa_olevat[0], uusi_nimi)
        print(f"[+] Solu luotu: {uusi_nimi}")

if __name__ == "__main__":
    replikoi_solut()
