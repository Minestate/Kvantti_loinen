from dna_ydin import hae_ydin, injektoi
# build_parasite.py
import os

def luo_nollatilat():
    tiedostot = [".bios_1.sys", ".bios_2.sys", ".bios_3.sys"]
    for nimi in tiedostot:
        # Luodaan täsmälleen 1024 tavun tiedosto, joka sisältää vain nollia (0x00)
        with open(nimi, "wb") as f:
            f.write(b'\x00' * 1024)
        print(f"[OK] Luotu nollatila: {nimi} (1024 tavua)")

if __name__ == "__main__":
    luo_nollatilat()
