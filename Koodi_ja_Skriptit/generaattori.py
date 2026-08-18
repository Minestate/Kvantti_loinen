from dna_ydin import hae_ydin, injektoi
import random
import textwrap
import pypdf  # HUOM: Muista asentaa komennolla: pip install pypdf

def lue_tiedosto(tiedostonimi):
    """Lukee tekstin joko .txt- tai .pdf-tiedostosta."""
    if tiedostonimi.lower().endswith('.pdf'):
        print(f"Avataan PDF-tiedostoa '{tiedostonimi}' ja pura tekstisisältöä...")
        teksti_lista = []
        
        # Avataan PDF binäärilukutilassa ('rb')
        with open(tiedostonimi, 'rb') as f:
            lukija = pypdf.PdfReader(f)
            # Käydään kaikki PDF:n sivut läpi ja poimitaan teksti
            for sivun_numero, sivu in enumerate(lukija.pages, 1):
                sivuteksti = sivu.extract_text()
                if sivuteksti:
                    teksti_lista.append(sivuteksti)
                
        # Yhdistetään kaikki sivut yhdeksi pitkäksi tekstiksi
        kokonais_teksti = "\n".join(teksti_lista)
        
        if not kokonais_teksti.strip():
            raise ValueError("PDF-tiedostosta ei löytynyt tekstiä. Onko kyseessä skannattu kuva-PDF?")
            
        return kokonais_teksti
    else:
        # Perinteinen tekstitiedoston luku
        with open(tiedostonimi, 'r', encoding='utf-8') as f:
            return f.read()

def tallenna_tiedosto(tiedostonimi, teksti):
    """Tallentaa generoidun kirjan uuteen tiedostoon."""
    with open(tiedostonimi, 'w', encoding='utf-8') as f:
        f.write(teksti)

def suora_luonti(teksti, max_sivuja=1000, sanoja_per_sivu=250):
    sanat = teksti.split()
    max_sanoja = max_sivuja * sanoja_per_sivu
    valittu_teksti = " ".join(sanat[:max_sanoja])
    return textwrap.fill(valittu_teksti, width=80)

def rakenna_markov_malli(teksti, n=2):
    sanat = teksti.split()
    malli = {}
    for i in range(len(sanat) - n):
        tila = tuple(sanat[i:i+n])
        seuraava_sana = sanat[i+n]
        if tila not in malli:
            malli[tila] = []
        malli[tila].append(seuraava_sana)
    return malli, sanat

def satunnainen_luonti(teksti, max_sivuja=1000, sanoja_per_sivu=250, n=2):
    malli, alkuperaiset_sanat = rakenna_markov_malli(teksti, n)
    if not malli:
        return "Teksti on liian lyhyt satunnaistetun mallin rakentamiseen."

    max_sanoja = max_sivuja * sanoja_per_sivu
    nykyinen_tila = random.choice(list(malli.keys()))
    generoitu_teksti = list(nykyinen_tila)

    for _ in range(max_sanoja - n):
        if nykyinen_tila in malli:
            seuraava_sana = random.choice(malli[nykyinen_tila])
            generoitu_teksti.append(seuraava_sana)
            nykyinen_tila = tuple(generoitu_teksti[-n:])
        else:
            nykyinen_tila = random.choice(list(malli.keys()))

    lopputulos = " ".join(generoitu_teksti)
    return textwrap.fill(lopputulos, width=80)

# --- PÄÄOHJELMA ---
if __name__ == "__main__":
    # Asetetaan uusi tiedostonimi tähän
    lahdetiedosto = "langennut_helvetin_enkeli.pdf"
    halutut_sivut = 1000
    
    try:
        alkuperainen_teksti = lue_tiedosto(lahdetiedosto)
        print(f"Teksti ladattu onnistuneesti (merkkejä yhteensä: {len(alkuperainen_teksti)}).")
        
        # 1. SUORA VERSIO
        print("Generoidaan suoraa versiota...")
        suora_kirja = suora_luonti(alkuperainen_teksti, max_sivuja=halutut_sivut)
        tallenna_tiedosto("suora_kirja.txt", suora_kirja)
        print("-> Suora kirja tallennettu: suora_kirja.txt")

        # 2. SATUNNAINEN REMIX-VERSIO
        print("Generoidaan satunnaistettua versiota...")
        satunnainen_kirja = satunnainen_luonti(alkuperainen_teksti, max_sivuja=halutut_sivut)
        tallenna_tiedosto("satunnainen_kirja.txt", satunnainen_kirja)
        print("-> Satunnainen kirja tallennettu: satunnainen_kirja.txt")

    except FileNotFoundError:
        print(f"VIRHE: Tiedostoa '{lahdetiedosto}' ei löytynyt samasta kansiosta.")
    except Exception as e:
        print(f"Tapahtui virhe: {e}")

