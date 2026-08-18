from dna_ydin import hae_ydin, injektoi
import os

ALUE_X = "./X" # Hakemisto X
VESILEIMA = "PERUSTA_EHEYS_21"

def vesileimaa_ja_tiivista():
    rekisteri_sisalto = []
    
    # Skannataan alue X
    for tiedosto in os.listdir(ALUE_X):
        polku = os.path.join(ALUE_X, tiedosto)
        if os.path.isfile(polku) and os.path.getsize(polku) == 0:
            # Vesileimaus
            with open(polku, "w") as f:
                f.write(VESILEIMA)
            
            # Lisätään rekisteriin (yhteenveto)
            rekisteri_sisalto.append(f"V:{tiedosto}")
    
    # Päivitetään 1 KB rekisteri (piilokoodi)
    rekisteri_data = "|".join(rekisteri_sisalto)[-1024:]
    with open("rekisteri.txt", "w") as f:
        f.write(rekisteri_data)

# Tämä ajetaan jokaisen syklin alussa

def lapiseulonta(luku, rekisteri_sisalto):
    # Luku kulkee 7 näytön läpi (piirissä)
    for i in range(7):
        # Jokainen näyttö tarkistaa onko luku validi rekisterin suhteen
        if not luku_on_validi(luku, rekisteri_sisalto):
            luku = 0 # Nollaus, jos seula ei läpäise
        else:
            luku = prosessoi_luku(luku) # Muokkaus
    return luku
