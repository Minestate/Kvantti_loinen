from dna_ydin import hae_ydin, injektoi
import time

class KestäväLankasulake:
    def __init__(self):
        self.kynnys_a = 3.0
        self.piikki_sieto = 0.5  # Sallitaan 0.5s piikit
        self.ylitys_aika = 0.0

    def valvo_virtaa(self, virta_a, delta_t):
        if virta_a > self.kynnys_a:
            self.ylitys_aika += delta_t
        else:
            self.ylitys_aika = max(0, self.ylitys_aika - delta_t * 2)

        if self.ylitys_aika > self.piikki_sieto:
            return False  # Sulake paloi
        return True  # Sulake kestää

def aja_vartiointi():
    vartija = KestäväLankasulake()
    print("=== KVANTTILOISEN 3A LANKASULAKE-VARTIOINTI ===")
    
    # Simuloidaan 10 sekunnin ajoa
    alkuaika = time.time()
    edellinen_aika = alkuaika
    
    try:
        while True:
            nyt = time.time()
            delta_t = nyt - edellinen_aika
            edellinen_aika = nyt
            
            # Simuloidaan virtaa (2.9A vakaa, välillä 3.1A piikki)
            virta_a = 2.9 + (0.3 if int(nyt) % 3 == 0 else 0)
            
            if not vartija.valvo_virtaa(virta_a, delta_t):
                print(f"\n!!! HÄLYTYS: 3A LANKASULAKE PALOI ({virta_a:.2f}A) !!!")
                break
            
            print(f"Vartiointi vakaa | Virta: {virta_a:.2f}A | Sulake: OK", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n[Vartiointi] Pysäytetty hallitusti.")

if __name__ == "__main__":
    aja_vartiointi()
