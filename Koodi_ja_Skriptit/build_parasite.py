from dna_ydin import hae_ydin, injektoi
import os

def luo_nollatila(nimi):
    """
    Luo täsmälleen 1 kilotavun (1024 tavua) tyhjän tiedoston.
    Tämä toimii isäntäjärjestelmän mekaanisena ankkurina.
    """
    try:
        with open(nimi, "wb") as f:
            # Kirjoitetaan 1024 tavua nollatilaa (0x00)
            f.write(b'\x00' * 1024)
        print(f"[ANKKURI] Luotu: {nimi} | Koko: {os.path.getsize(nimi)} tavua")
    except Exception as e:
        print(f"[VIRHE] Ankkurin luonti epäonnistui: {e}")

def main():
    print("=== QUANTUM-PARASITE: BOOTSTRAP GENERATOR ===")
    tiedostot = [".bios_1.sys", ".bios_2.sys", ".bios_3.sys"]
    
    for nimi in tiedostot:
        if os.path.exists(nimi):
            print(f"[INFO] Ankkuri {nimi} on jo olemassa. Ohitetaan.")
        else:
            luo_nollatila(nimi)
            
    print("\n[VALMIS] Järjestelmän nollatilat ankkuroitu.")
    print("Quantum-parasite on nyt valmis tulkitsemaan näitä tyhjiöitä.")

if __name__ == "__main__":
    main()
