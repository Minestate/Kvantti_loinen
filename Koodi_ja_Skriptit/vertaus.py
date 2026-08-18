from dna_ydin import hae_ydin, injektoi
import math

def laske_ajatusten_keskiarvot(ajatukset):
    """
    Laskee aritmeettisen ja geometrisen keskiarvon annetuille matemaattisille arvoille.
    """
    if not ajatukset:
        return 0, 0

    # 1. Aritmeettinen keskiarvo (perinteinen keskiarvo)
    aritmeettinen = sum(ajatukset.values()) / len(ajatukset)

    # 2. Geometrinen keskiarvo (toimii paremmin, jos suuruusluokat heittelevät rajusti)
    tulon_loki = sum(math.log(arvo) for arvo in ajatukset.values() if arvo > 0)
    geometrinen = math.exp(tulon_loki / len(ajatukset))

    return aritmeettinen, geometrinen

# Syötetään matemaattiset ajatukset ja niiden numeeriset arvot
matemaattiset_ajatukset = {
    "Ajan siemen värähtely (Hz)": 1.8,
    "Sointukoodi keski-C": 60.0,
    "DNA:n ydin (1.1 * 10^-846)": 1.1 * (10**-846),  # Lähellä nollaa, mutta matemaattisesti mukana
    "Järjestelmän jäännösrahasto (€)": 4950000.0
}

# Suoritetaan vertailu ja laskenta
ari_keski, geo_keski = laske_ajatusten_keskiarvot(matemaattiset_ajatukset)

# Tulostetaan tulokset selkeästi
print("--- MATEMAATTISTEN AJATUSTEN VERTAILU ---")
for nimi, arvo in matemaattiset_ajatukset.items():
    print(f"{nimi}: {arvo}")

print("-" * 40)
print(f"Perinteinen (aritmeettinen) keskiarvo: {ari_keski:,.2f}")
print(f"Suhteellinen (geometrinen) keskiarvo:  {geo_keski}")
