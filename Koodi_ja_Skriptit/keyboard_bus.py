from dna_ydin import hae_ydin, injektoi
class KeyboardBus:
    def __init__(self, core):
        self.core = core
        self.buffer = []

    def capture_keystroke(self, key):
        # Kerätään "ryysäkkä" sanoja
        self.buffer.append(key)
        if len(self.buffer) > 5:  # Kun saavutetaan 5 kirjaimen "tärinä"
            word = "".join(self.buffer)
            self.core.process_etymology(len(word))
            self.buffer = [] # Tyhjennetään rysäkkä
