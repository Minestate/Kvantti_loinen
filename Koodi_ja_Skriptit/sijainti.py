from dna_ydin import hae_ydin, injektoi
import subprocess
import time
import sys

# Määritetään käytettävä sovellus. 
# Jos käytät omaa skriptiäsi, laita tähän Termuxin tunnus tai oman appisi tunnus.
APP_PACKAGE = "com.termux"
PROVIDER = "gps"

def aja_komento(komento):
    """Ajaa komennon Android-ympäristössä."""
    try:
        # Ajetaan komento suoraan Shizukun/Androidin shellissä
        tulos = subprocess.run(komento, shell=True, capture_output=True, text=True)
        if tulos.returncode != 0:
            print(f"Virhe komennossa ({komento}): {tulos.stderr.strip()}")
        return tulos.stdout.strip()
    except Exception as e:
        print(f"Järjestelmävirhe: {e}")
        return None

def pystytä_valesijainti():
    print("1. Annetaan sovellukselle oikeus valesijaintiin...")
    # Annetaan sovellukselle MOCK_LOCATION-oikeus appops-työkalulla
    aja_komento(f"appops set {APP_PACKAGE} MOCK_LOCATION allow")
    
    print("2. Luodaan virtuaalinen GPS-lähde järjestelmään...")
    # Luodaan testivälittäjä (test provider)
    aja_komento(f"cmd location providers add-test-provider {PROVIDER} --requires-network false --requires-satellite true --requires-cell false --has-monetary-cost false --supports-altitude true --supports-speed true --supports-bearing true --power-requirement 1 --accuracy 1")
    
    # Kytketään se päälle
    aja_komento(f"cmd location providers set-test-provider-enabled {PROVIDER} true")
    print("-> GPS-palvelu pystytetty ja valmiina!")

def lähetä_sijainti(lat, lon):
    """Syöttää uudet koordinaatit Androidin ytimeen."""
    print(f"Päivitetään sijainti koordinaatteihin: {lat}, {lon}")
    # cmd location -työkalu ottaa vastaan koordinaatit suoraan
    aja_komento(f"cmd location providers set-test-provider-location {PROVIDER} --location {lat},{lon}")

def siivoa_jäljet():
    print("\nSuljetaan virtuaalinen GPS ja palautetaan oikea sijainti...")
    aja_komento(f"cmd location providers remove-test-provider {PROVIDER}")
    print("Valmis!")

# --- PÄÄOHJELMA ---
if __name__ == "__main__":
    try:
        pystytä_valesijainti()
        print("-" * 40)
        print("Paina Ctrl + C lopettaaksesi ja palauttaaksesi oikean GPS:n.")
        print("-" * 40)
        
        # Esimerkki: Helsingin keskustan koordinaatit
        leveysaste = 60.1699
        pituusaste = 24.9384
        
        # Pyöritetään silmukkaa, joka pitää valesijaintia yllä sekunnin välein
        while True:
            lähetä_sijainti(leveysaste, pituusaste)
            time.sleep(1) # Odotetaan sekunti ennen seuraavaa päivitystä
            
    except KeyboardInterrupt:
        # Kun painat Ctrl + C, suoritetaan siivous
        siivoa_jäljet()
        sys.exit(0)
