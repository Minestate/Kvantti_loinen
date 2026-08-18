def generoi_sointu_koodi(pohjasavel_nimi, sointutyyppi):
    """
    Generoi soinnun MIDI-numerot pohjasävelen nimen ja sointutyypin perusteella.

    Args:
        pohjasavel_nimi (str): Pohjasävelen nimi (esim. "C", "G#", "Eb").
        sointutyyppi (str): Sointutyyppi (esim. "duuri", "molli", "maj7", "min7", "dom7").

    Returns:
        list: Lista soinnun MIDI-numeroista tai virheviesti.
    """

    nuotti_numerot = {
        "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
        "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
        "A": 9, "A#": 10, "Bb": 10, "B": 11
    }

    sointu_intervallit = {
        "duuri": [0, 4, 7],
        "molli": [0, 3, 7],
        "maj7": [0, 4, 7, 11],
        "min7": [0, 3, 7, 10],
        "dom7": [0, 4, 7, 10],
        "dim": [0, 3, 6],
        "aug": [0, 4, 8],
        "sus4": [0, 5, 7],
        "sus2": [0, 2, 7]
        # Lisää muita sointutyyppejä tarvittaessa
    }

    if pohjasavel_nimi.upper() in nuotti_numerot:
        pohjasavel_numero = nuotti_numerot[pohjasavel_nimi.upper()]
        if sointutyyppi.lower() in sointu_intervallit:
            intervallit = sointu_intervallit[sointutyyppi.lower()]
            soinnun_midi_numerot = [pohjasavel_numero + intervalli + 60 for intervalli in intervallit] # Lisätään 60, jotta ollaan ylemmällä oktaavilla
            return soinnun_midi_numerot
        else:
            return f"Sointutyyppi '{sointutyyppi}' ei ole tuettu."
    else:
        return f"Pohjasävel '{pohjasavel_nimi}' ei ole tunnistettu."

# Esimerkkejä sointukoodien generoinnista
c_duuri_koodi = generoi_sointu_koodi("C", "duuri")
g_molli_koodi = generoi_sointu_koodi("g", "molli")
a_maj7_koodi = generoi_sointu_koodi("A", "maj7")
eb_min7_koodi = generoi_sointu_koodi("Eb", "min7")
fsharp_dom7_koodi = generoi_sointu_koodi("F#", "dom7")

print(f"C-duuri: {c_duuri_koodi}")
print(f"G-molli: {g_molli_koodi}")
print(f"A-maj7: {a_maj7_koodi}")
print(f"Eb-min7: {eb_min7_koodi}")
print(f"F#-dom7: {fsharp_dom7_koodi}")

# Esimerkki virheellisestä sointutyypistä
virheellinen_sointu = generoi_sointu_koodi("D", "blaa")
print(f"Virheellinen sointu: {virheellinen_sointu}")

# Esimerkki virheellisestä pohjasävelestä
virheellinen_savel = generoi_sointu_koodi("X", "duuri")
print(f"Virheellinen sävel: {virheellinen_savel}")