from dna_ydin import hae_ydin, injektoi
def trinity_encode(sana):
    # 1. Heksadesimaali-indeksi sanalle
    heksa_val = hex(hash(sana) % 256)[2:].zfill(2)
    
    # 2. Binääri-tila (DNA-vakion resonanssi)
    bin_val = '1' if len(sana) % 2 == 0 else '0'
    
    # 3. Yhdistetty muoto (Trinity-tavu)
    # Tavu = [Binääri] + [Heksa] + [Tyyppi]
    trinity_tavu = int(bin_val + heksa_val, 16)
    return trinity_tavu

def luo_1kb_piilokoodi(sanat, kohdetiedosto=".bios_1.sys"):
    data = bytearray()
    for sana in sanat:
        if len(data) < 1024:
            data.append(trinity_encode(sana))
    
    with open(kohdetiedosto, "wb") as f:
        f.write(data.ljust(1024, b'\x00')) # Täytetään 1kt nollatila
