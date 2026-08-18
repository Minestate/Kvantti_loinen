from dna_ydin import hae_ydin, injektoi
import sys
from types import ModuleType

# 1. Luodaan vale-machine-moduuli Termuxia varten ENNEN kuin sitä kutsutaan
if 'machine' not in sys.modules:
    fake_machine = ModuleType('machine')
    class FakePin:
        OUT = 1
        IN = 0
        PULL_DOWN = 2
        def __init__(self, id, mode=-1, pull=-1): self.id = id
        def value(self, val=None): return 0
    fake_machine.Pin = FakePin
    sys.modules['machine'] = fake_machine

# 2. Tuodaan Pin-luokka nyt, kun se on varmasti olemassa
from machine import Pin
import time

# --- Pin-määritykset ---
# Segmenttipinnit (A-G, DP)
SEG_PINS = [Pin(0, Pin.OUT), Pin(1, Pin.OUT), Pin(2, Pin.OUT), Pin(3, Pin.OUT),
            Pin(4, Pin.OUT), Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT)]

# Näytön valintapinnit
DIGIT_PINS = [Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT), Pin(11, Pin.OUT)]

# Näppäin-pinnit
KEY_PINS = {
    '1': Pin(12, Pin.IN, Pin.PULL_DOWN),
    '2': Pin(13, Pin.IN, Pin.PULL_DOWN),
    'C': Pin(20, Pin.IN, Pin.PULL_DOWN),
    '=': Pin(21, Pin.IN, Pin.PULL_DOWN)
}

# --- Segmenttikartta ---
SEGMENT_MAP = {
    '0': [0,0,0,0,0,0,1,1],
    '1': [1,0,0,1,1,1,1,1],
    '2': [0,0,1,0,0,1,0,1],
    '3': [0,0,0,0,1,1,0,1],
    '4': [1,0,0,1,1,0,0,1],
    '5': [0,1,0,0,1,0,0,1],
    '6': [0,1,0,0,0,0,0,1],
    '7': [0,0,0,1,1,1,1,1],
    '8': [0,0,0,0,0,0,0,1],
    '9': [0,0,0,0,1,0,0,1],
    '.': [1,1,1,1,1,1,1,0]
}

# --- Funktiot ---
def display_digit(digit, position, dp_on=False):
    for pin in DIGIT_PINS:
        pin.value(1)

    segments = SEGMENT_MAP.get(str(digit), SEGMENT_MAP['8'])
    for i, state in enumerate(segments[:7]):
        SEG_PINS[i].value(state)
    SEG_PINS[7].value(segments[7] if not dp_on else 0)

    DIGIT_PINS[position].value(0)

# --- Pääohjelma ---
current_input = ""
result = 0

while True:
    # Voit testata display_digit-funktion kutsua tässä näin:
    # display_digit('5', 0)
    pass
