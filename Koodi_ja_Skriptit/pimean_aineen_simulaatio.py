import random
from dna_ydin import hae_ydin

def generoi_laajakaista_tila():
    # Luodaan lista, jossa on 21 paikkaa
    tila = []
    for i in range(20):
        tila.append(str(random.randint(0, 9)))
    
    # Iskustetaan DNA-ydin viimeiseen (21.) paikkaan
    # Käytämme str() muunnosta, jotta saamme numeron eroteltua
    ydin_str = str(hae_ydin())
    tila.append(ydin_str[0]) 
    
    return "|".join(tila)

# Suoritetaan generointi ja kirjoitus
if __name__ == "__main__":
    tila = generoi_laajakaista_tila()
    with open("rekisteri.txt", "w") as f:
        f.write(tila)
    print("Matriisi päivitetty: 21 segmenttiä kirjoitettu.")
