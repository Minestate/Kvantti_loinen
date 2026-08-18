import random

# Esimerkki: Kartta edustaa timanttiesiintymiä (koordinaatit)
# ja niiden vaikutusta ennustettavaan sanaan.
diamond_map_nodes = {
    "Suomi": {"timantti": 0.1, "kallio": 0.8, "geologia": 0.1},
    "Afrikka": {"timantti": 0.7, "kallio": 0.2, "geologia": 0.1},
    "Siperia": {"timantti": 0.4, "kallio": 0.5, "geologia": 0.1}
}

def ennusta_seuraava_sana(sijainti):
    """
    Simuloi ennakoivaa syöttöä, joka painottaa 
    valintaa kyseisen sijainnin geologisen 'piirilevyn' mukaan.
    """
    if sijainti in diamond_map_nodes:
        painot = diamond_map_nodes[sijainti]
        # Arvotaan sana painotetusti
        sanat = list(painot.keys())
        todennakoisyydet = list(painot.values())
        return random.choices(sanat, weights=todennakoisyydet, k=1)[0]
    return "tuntematon"

# Käyttöesimerkki
nykyinen_sijainti = "Afrikka"
print(f"Ennuste sijainnista {nykyinen_sijainti}: {ennusta_seuraava_sana(nykyinen_sijainti)}")