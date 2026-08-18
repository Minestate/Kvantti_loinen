from dna_ydin import hae_ydin, injektoi
import math
import subprocess
import struct
import sys

# 1. MÄÄRITELMÄT
SAMPLE_RATE = 44100  # Kuinka monta näytettä sekunnissa
DURATION = 3.0       # Soinnun kesto sekunteina

# Valitaan soinnun taajuudet (Hz). Tässä esim. A-molli (A4, C5, E5)
CHORD_FREQUENCIES = [440.00, 523.25, 659.25]

# Kytketään yhteys SoX-ohjelmaan (avaat putken taustaprosessiin)
sox_command = ['play', '-t', 'raw', '-r', str(SAMPLE_RATE), '-e', 'floating-point', '-b', '32', '-c', '1', '-']
try:
    process = subprocess.Popen(sox_command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    print("Virhe: Muistithan asentaa SoX:in (pkg install sox)?", file=sys.stderr)
    sys.exit(1)

# 2. ÄÄNEN GENERIOINTI (Matemaattinen silmukka)
# Lasketaan kuinka monta näytettä yhteensä tarvitaan
total_samples = int(SAMPLE_RATE * DURATION)

print("Soitetaan sointu...")

for i in range(total_samples):
    # Lasketaan nykyinen aika sekunteina
    t = i / SAMPLE_RATE
    
    # --- SINUN TEHTÄVÄSI NRO 1 ---
    # Meidän täytyy laskea kaikkien CHORD_FREQUENCIES-listan taajuuksien
    # siniaallot yhteen tässä ajanhetkessä 't'.
    # Kaava yksittäiselle aallolle: math.sin(2 * math.pi * f * t)
    
    yhteissumma = 0.0
    for f in CHORD_FREQUENCIES:
        yhteissumma += math.sin(2 * math.pi * f * t)
    
    # --- SINUN TEHTÄVÄSI NRO 2 ---
    # Koska laskimme kolme aaltoa yhteen, 'yhteissumma' voi olla välillä [-3.0, 3.0].
    # SoX odottaa standardia liukulukua, joka pysyy visusti välillä [-1.0, 1.0].
    # Miten skaalaat tai normalisoit 'yhteissumma'-muuttujan tässä kohtaa?
    
    soiva_nayte = yhteissumma / 3.0  # Tässä yksi tapa, keksitkö paremman?

    # 3. DATAN MUUTTAMINEN TAVUIKSI JA LÄHETYS
    # Muutetaan Pythonin float-luku 32-bittiseksi raakatavuksi ('f' = float)
    dataa_tavuina = struct.pack('f', soiva_nayte)
    
    # Työnnetään tavu putkesta sisään SoXille
    try:
        process.stdin.write(dataa_tavuina)
    except IOError:
        # Jos soitto katkaistaan kesken
        break

# Suljetaan putki ja odotetaan, että SoX lopettaa
process.stdin.close()
process.wait()
print("Sointu päättyi.")
