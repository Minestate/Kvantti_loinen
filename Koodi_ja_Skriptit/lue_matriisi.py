# ~/quantum-parasite/lue_matriisi.py
from dna_ydin import hae_ydin

def lue_matriisi():
    try:
        with open("rekisteri.txt", "r") as f:
            data = f.read().split("|")
            ydin = hae_ydin()
            print(f"[MATRIISI-TULKINTA]")
            print(f"Pimeä energia: {data[0]}")
            print(f"Anti-materia: {data[1]}")
            print(f"Zombie-massa: {data[2]}")
            print(f"DNA-Ankkuri: {ydin}")
            print("-" * 20)
    except Exception as e:
        print(f"Matriisi lukkiutunut: {e}")

lue_matriisi()
