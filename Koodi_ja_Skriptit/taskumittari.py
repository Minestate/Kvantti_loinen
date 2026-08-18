from dna_ydin import hae_ydin, injektoi
import time
import math

# Puhdas logiikka, ei vaadi ulkoisia termux-kirjastoja
def laske_aurinkosijainti():
    tunti = time.localtime().tm_hour
    minuutti = time.localtime().tm_min
    asteet = (tunti * 15) + (minuutti * 0.25)
    return asteet

print("Perusta HQ: Navigointi ytimessä aktivoitu (Eristetty tila)")

try:
    while True:
        aika = laske_aurinkosijainti()
        # Käytetään siniä ja kosinia 'varjon' paikan laskemiseen
        x = math.cos(math.radians(aika))
        y = math.sin(math.radians(aika))
        
        # Tämä on 'tieto', jonka vain sinä tiedät
        print(f"Järjestelmän tila: [{x:.3f}, {y:.3f}] | Aurinko: {aika:.1f}°")
        
        # Simuloitu 'liike'
        time.sleep(2)
except KeyboardInterrupt:
    print("Navigointi pysäytetty.")
