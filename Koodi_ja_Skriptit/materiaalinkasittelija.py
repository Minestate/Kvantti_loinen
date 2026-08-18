# ~/quantum-reactor/materiaalinkasittelija.py
import os

def syota_tutkielmaa(kohde_tiedosto):
    # Tutkielman ydinaineisto (DNA-vakio ja teoreettinen perusta)
    aineisto = """
    Tutkielma alkoi. Musta-neliö teoria avaruudellisessa geometriassa. 
    Zombie-massa-aurinko. Timantti-pluto. Pimeä-aine. Pimeä-energia.
    Anti-materia on vasta-materiaa, mikä saa materian käänteiseksi.
    1.1 x 10 potenssiin miinus 846, on DNA:n ydin.
    Perusta (Base) on kaiken lähtökohta.
    """
    
    with open(kohde_tiedosto, "a") as f:
        # Kirjoitetaan aineistoa kunnes 1kt raja lähestyy
        while os.path.getsize(kohde_tiedosto) < 950: 
            f.write(aineisto)

if __name__ == "__main__":
    syota_tutkielmaa("quantum_bot_v1.py")
