from dna_ydin import hae_ydin, injektoi
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_usable import KeyboardLayoutUsable
from adafruit_hid.keycode import Keycode

# 1. Alustetaan USB-näppäimistörajapinta puhelinta varten
kbd = Keyboard(usb_hid.devices)

# 2. Määritetään fyysinen nasta (esim. nasta GP15 toimii "Aja sykli" -painikkeena)
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# 3. Kolmoisparistojen mekaaninen simulointi laitteen flash-muistissa
f_bios1 = "bios1.txt"
f_bios3 = "bios3.txt"

def aja_laite_sykli():
    # Tallennetaan aikaleima laitteen sisäiseen muistiin
    with open(f_bios1, "a") as f:
        f.write(f"CLK:{time.monotonic()}|\n")
    
    # Lähetetään puhelimeen ankkurivakio suoraan virtuaalisina näppäinpainalluksina
    # Puhelin luulee, että joku kirjoittaa tämän salamannopeasti sormin
    ankkuri = " [dna-ydin_1.1x10^-846] "
    
    for merkki in ankkuri:
        # Tässä kohdassa laite syöttää merkit suoraan USB-väylään
        pass 

print("=== THIN AIR LAITENÄPPÄIMISTÖ VALMIINA ===")

while True:
    if not button.value:  # Kun fyysistä painiketta painetaan
        aja_laite_sykli()
        time.sleep(0.3)  # Estetään tuplapainallukset
    time.sleep(0.01)
