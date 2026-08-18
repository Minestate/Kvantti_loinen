from dna_ydin import hae_ydin, injektoi
import signal
import sys

def pakota_vastavirta(signum, frame):
    print("[SIGNAL] Bash lähetti vastavirta-käskyn!")
    # Tässä kohtaa kello kääntyy vastapäivään
    laskuri.käännä_suunta()

signal.signal(signal.SIGUSR1, pakota_vastavirta)
