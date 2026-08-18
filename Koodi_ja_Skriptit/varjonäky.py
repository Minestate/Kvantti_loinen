from dna_ydin import hae_ydin, injektoi
import time
import math

def lue_aurinkosijainti():
    # Käytetään laitteen kelloa simuloimaan auringon kiertoa
    # Tämä on "Perusta HQ":n oma koordinaatisto
    tunti = time.localtime().tm_hour
    minuutti = time.localtime().tm_min
    
    # Aurinko liikkuu 15 astetta tunnissa
    asteet = (tunti * 15) + (minuutti * 0.25)
    return asteet

def varjon_paikka(asteet):
    # Lasketaan missä kohtaa 'taivasta' (järjestelmän tilaa) olemme
    x = math.cos(math.radians(asteet))
    y = math.sin(math.radians(asteet))
    return x, y

print("Aurinkokello on synkronoitu. Navigointi ilman ulkoista GPS:ää aloitettu.")
while True:
    aika = lue_aurinkosijainti()
    x, y = varjon_paikka(aika)
    print(f"HQ Sijainti (varjon koordinaatit): X={x:.4f}, Y={y:.4f}")
    time.sleep(1)
