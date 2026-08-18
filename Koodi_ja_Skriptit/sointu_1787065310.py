from dna_ydin import hae_ydin, injektoi
import math
import subprocess
import struct
import sys

# 1. PERUSASETUKSET
SAMPLE_RATE = 44100  # Näytteenottotaajuus (Hz)
DURATION = 0.4       # Yhden merkin soinnun kesto sekunteina (esim. 0.4 sekuntia)

# Mitä tekstiä tai numeroita haluat laitteen soittavan?
# Voit muuttaa tätä vapaasti!
SYOTE = "123 ABC"

# 2. KONSEPTI: MERKIN MUUTTAMINEN SOINNUKSI
def merkki_soinnuksi(merkki):
    if merkki == " ":
        # Välilyönti palauttaa nollataajuudet (hiljaisuus)
        return [0.0, 0.0, 0.0]
        
    # Haetaan merkin numeerinen ASCII-arvo (esim. '1'=49, 'A'=65)
    perus_arvo = ord(merkki)
    
    # Lasketaan perustaajuus niin, että se osuu mukavalle kuuloalueelle
    perustaajuus = 150.0 + (perus_arvo * 3.0)
    
    # Luodaan harmoninen kolmisointu matemaattisilla suhteilla (perussävel, terssi, kvintti)
    terssi = perustaajuus * 1.25
    kvintti = perustaajuus * 1.50
    
    return [perustaajuus, terssi, kvintti]

# 3. YHTEYS SOX-OHJELMAAN
# Tämän pitää olla täsmälleen näin, jotta liput ja heittomerkit täsmäävät:
sox_command = ['play', '-t', 'raw', '-r', str(SAMPLE_RATE), '-e', 'floating-point', '-b', '32', '-c', '1', '-']

try:
    # Tästä puuttui loppuosa! Ohjataan tulosteet piiloon, etteivät ne sotke Termuxia
    process = subprocess.Popen(sox_command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    print("SoX puuttuu!")

except FileNotFoundError:
    print("Virhe: Asenna SoX ensin Termuxiin komennolla: pkg install sox", file=sys.stderr)
    sys.exit(1)

print(f"Käännetään teksti '{SYOTE}' musiikiksi...")

# 4. PÄÄSILMUKKA: KÄYDÄÄN TEKSTI LÄPI MERKKI MERKILTÄ
for merkki in SYOTE:
    # Haetaan merkkikohtaiset taajuudet
    taajuudet = merkki_soinnuksi(merkki)
    
    # Lasketaan kuinka monta näytettä tämä yksi merkki tarvitsee
    samples_per_char = int(SAMPLE_RATE * DURATION)
    
    for i in range(samples_per_char):
        t = i / SAMPLE_RATE
        
        # Generoidaan ja summataan kolme siniaaltoa lennosta
        yhteissumma = 0.0
        for f in taajuudet:
            if f > 0:  # Jos taajuus on nolla (välilyönti), pysytään hiljaa
                yhteissumma += math.sin(2 * math.pi * f * t)
        
        # Normalisoidaan ääni jakamalla signaali kolmella, jotta se ei säröydy
        soiva_nayte = yhteissumma / 3.0
        
        # Muutetaan näyte 32-bittiseksi liukulukutavuksi ja lähetetään SoXille
        dataa_tavuina = struct.pack('f', soiva_nayte)
        try:
            process.stdin.write(dataa_tavuina)
        except IOError:
            break

# Suljetaan putki kun kaikki merkit on soitettu
process.stdin.close()
process.wait()
print("Soitto päättyi menestyksekkäästi!")
