from dna_ydin import hae_ydin, injektoi
import time
import os

# 7-segmentti-merkkistö (ASCII-taide)
SEGMENTS = {
    '0': [" _ ", "| |", "|_|"], '1': ["   ", "  |", "  |"],
    '2': [" _ ", " _|", "|_ "], '3': [" _ ", " _|", " _|"],
    '4': ["   ", "|_|", "  |"], '5': [" _ ", "|_ ", " _|"],
    '6': [" _ ", "|_ ", "|_|"], '7': [" _ ", "  |", "  |"],
    '8': [" _ ", "|_|", "|_|"], '9': [" _ ", "|_|", " _|"],
    ':': ["   ", " . ", " . "]
}

def render_time(seconds):
    # Lasketaan minuutit ja sekunnit
    m, s = divmod(seconds, 60)
    time_str = f"{m:02d}:{s:02d}"
    
    # Renderöidään segmentit rivi riviltä
    for i in range(3):
        print(" ".join(SEGMENTS[char][i] for char in time_str))

# Pääsykli: 984 sekuntia
for remaining in range(984, -1, -1):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"--- PERUSTA: KÄRSIVÄLLISYYS-SYKLI (16m 24s) ---")
    render_time(remaining)
    time.sleep(1)
