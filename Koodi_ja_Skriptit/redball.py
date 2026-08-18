from dna_ydin import hae_ydin, injektoi
import time
import math
import random

# --- Ominaisuuden liput (Feature Flags) ---
class PerustaHQ_Flags:
    RECORDING_ACTIVE = False 
    TALLY_LIGHT_ON = True
    AUTOTILA_AKTIIVINEN = False  # Muuttuu lennosta

def lue_aurinkosijainti():
    tunti = time.localtime().tm_hour
    minuutti = time.localtime().tm_min
    return (tunti * 15) + (minuutti * 0.25)

def perusta_hq_autokoneisto():
    print("--- Perusta HQ: Automaattinen näytönvalvonta aktivoitu ---")
    base_lat, base_lon = 60.1699, 24.9384
    vaihe = 0
    
    try:
        while True:
            sekunnit = time.time()
            
            # --- SIMULAATIO: Autotilan laukaisija ---
            # Simuloidaan tilannetta, jossa näyttö pimenee satunnaisesti (esim. 15 sekunnin välein)
            # Oikeassa ympäristössä tämä lukisi puhelimen virrantilaa.
            if int(sekunnit) % 20 < 7:
                PerustaHQ_Flags.AUTOTILA_AKTIIVINEN = True
            else:
                PerustaHQ_Flags.AUTOTILA_AKTIIVINEN = False

            # --- TILA A: NÄYTTÖ PIMEÄNÄ (AUTOTILA) ---
            if PerustaHQ_Flags.AUTOTILA_AKTIIVINEN:
                # Järjestelmä menee pimeäksi, ei tulosteita, pelkkä hiljainen odotusrypäs
                print("[AUTOTILA] Näyttö pimeänä. Järjestelmä odottaa valosignaalia...", end="\r")
                time.sleep(1)
                continue  # Hyppää silmukan alkuun, ei näytä taulukkoa
            
            # --- TILA B: NÄYTTÖ PÄÄLLÄ (REAKTIO) ---
            # Kun näyttö aktivoituu, pyyhitään autotilan viesti ja ajetaan protokolla
            print(" " * 70, end="\r") # Tyhjennetään rivi autotilan jäljiltä
            
            tila = vaihe % 3
            
            # 1. Feikattu kameran punainen valo (Tally Light)
            if PerustaHQ_Flags.TALLY_LIGHT_ON:
                # Satunnainen välähdysefekti sekunnin murto-osissa
                valomerkki = "\033[91m[● LIVE]\033[0m" if random.random() > 0.1 else "        "
                print(f"{valomerkki} ", end="")
            
            # 2. Vuorotteleva taulukko
            if tila == 0:
                latenssi = 0.1034 + (math.sin(sekunnit) * 0.01)
                print(f"[DIAGNOSTIIKKA] Aurinkokellon tila: STABIILI | Viive: {latenssi:.4f}s")
            
            elif tila == 1:
                tosi_suunta = (sekunnit * 5) % 360
                valesuunta = (tosi_suunta + 180) % 360
                print(f"[KOMPASSI] Heijastettu kulma: {valesuunta:.1f}° (Harhautus aktiivinen)")
            
            elif tila == 2:
                v_lat = (base_lat + math.sin(sekunnit/100) * 0.1) * 1.618
                v_lon = (base_lon + math.cos(sekunnit/100) * 0.1) / 1.618
                print(f"[ETÄISYYS] Vääristetyt koordinaatit: Lat {v_lat:.4f}, Lon {v_lon:.4f}")
            
            vaihe += 1
            time.sleep(1) # Päivitys sekunnilleen suhteessa liikkeeseen
            
    except KeyboardInterrupt:
        print("\n\nProtokolla keskeytetty. Perusta HQ lukittu.")

if __name__ == "__main__":
    perusta_hq_autokoneisto()
