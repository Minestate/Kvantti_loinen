from dna_ydin import hae_ydin, injektoi
import time
import random

def simuloi_wifi_signaali():
    # Simuloitu signaalin voimakkuus (dBm)
    signaali = random.randint(-80, -30)
    print(f"[ISOÄLY - WI-FI] Signaali: {signaali} dBm")
    
    # Valvotaan parametreja: jos signaali heikko, isoäly tekee korjausliikkeen
    if signaali < -70:
        print("[ISOÄLY] VAROITUS: Parametrien eheys heikentynyt. Suoritetaan synkronointi.")
        return "SYNC_REQUIRED"
    return "STABLE"

if __name__ == "__main__":
    print("[ISOÄLY] Langaton valvontayhteys kytketty...")
    while True:
        tila = simuloi_wifi_signaali()
        # Kirjoitetaan tila 'isoaly_status.txt' tiedostoon, jota emolevy lukee
        with open("isoaly_status.txt", "w") as f:
            f.write(tila)
        time.sleep(5) # Wi-Fi-kortin päivitysväli
