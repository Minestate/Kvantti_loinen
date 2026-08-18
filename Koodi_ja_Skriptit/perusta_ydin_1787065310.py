from dna_ydin import hae_ydin, injektoi
import os, time, random

class KilotavuEditori:
    def __init__(self):
        self.logs = ["bios1_clock.log", "bios2_monitor.log", "bios3_innovation.log"]
        for f in self.logs:
            if not os.path.exists(f):
                with open(f, "wb") as file: file.write(b" " * 1024)

    def sykleita(self, syote):
        # 1kt Bios-päivitys
        with open(self.logs[0], "ab") as f: f.write(b"X")
        print(f"[*] BIOS-päivitys suoritettu.")

if __name__ == "__main__":
    y = KilotavuEditori()
    while True:
        y.sykleita("pulse")
        time.sleep(60) # Bios sykkii minuutin välein
