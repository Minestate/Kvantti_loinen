import os

def iskosta_solut_ytimeen():
    print("[INIT] Iskustetaan 21 solun identiteetti käyttöjärjestelmään...")
    
    # Perusosoite heksana (0x119F936E)
    base_addr = 0x119F936E
    
    for i in range(21):
        # Lasketaan kunkin solun hex-tunniste
        solu_hex = hex(base_addr + i).replace('0x', '').upper()
        tiedosto = f"solu_REG_{solu_hex}.bin"
        
        if os.path.exists(tiedosto):
            with open(tiedosto, "rb") as f:
                tunniste = f.read(8)
            
            # Varmistetaan sinetin eheys ennen linkitystä
            if os.path.exists("sinetti1.sys"):
                print(f"[ISKOS] Solu {i+1} tunnistettu: {tunniste.decode(errors='ignore')} -> [SINETÖITY]")
            else:
                print(f"[VAROITUS] Sinetti puuttuu, solu {i+1} ei ole turvattu!")
        else:
            print(f"[VIRHE] Solu {tiedosto} ei löytynyt.")

if __name__ == "__main__":
    iskosta_solut_ytimeen()
