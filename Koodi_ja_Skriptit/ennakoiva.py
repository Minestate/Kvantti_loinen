from dna_ydin import hae_ydin, injektoi
import time
import random
import os
import subprocess  # Tarvitaan Termuxin komentorivikutsuja varten
import json

class KilotavuEditori:
    def __init__(self, hz=60):
        self.hz = hz
        self.sykli_kesto = 1.0 / hz

        # Tiedostot, jotka toimivat 1 kt paristoina
        self.f_bios1 = "bios1_clock.log"
        self.f_bios2 = "bios2_monitor.log"
        self.f_bios3 = "bios3_innovation.log"

        # Alustetaan tiedostot vakiokokoisiksi (1 kt tyhjää tilaa aluksi)
        self._varmista_1kt_koko()

    def _varmista_1kt_koko(self):
        """Varmistaa että tiedostot ovat olemassa ja toimivat 1 kt rajassa"""
        for f in [self.f_bios1, self.f_bios2, self.f_bios3]:
            if not os.path.exists(f):
                with open(f, "wb") as file:
                    file.write(b" " * 1024) # Täytetään 1024 tavulla (1 kt)

    def _kirjoita_piiloloki(self, tiedosto, data_str):
        """Kirjoittaa dataa 1 kt tiedostoon säilyttäen tarkan koon"""
        try:
            with open(tiedosto, "rb") as file:
                nykyinen = file.read().replace(b" ", b"") # Poistetaan tyhjät

            # Yhdistetään uusi piilokoodi vanhaan
            uusi_data = nykyinen + data_str.encode('utf-8') + b"|"

            # Jos menee yli 1 kt, leikataan alusta (vanhat paristotiedot kuluvat pois)
            if len(uusi_data) > 1024:
                uusi_data = uusi_data[-1024:]
            else:
                # Täytetään loppu tyhjällä, jotta koko on aina TASAN 1024 tavua (1 kt)
                uusi_data = uusi_data.ljust(1024, b" ")

            with open(tiedosto, "wb") as file:
                file.write(uusi_data)
        except Exception:
            pass

    def lue_sanavarasto(self):
        """Lukee BIOS 3 tiedostosta ennakoidut uudet sanat"""
        if not os.path.exists(self.f_bios3):
            return set()
        with open(self.f_bios3, "rb") as file:
            sisalto = file.read().decode('utf-8', errors='ignore').strip()
        sanat = [s for s in sisalto.split("|") if s.strip()]
        return set(sanat)

    def _kutsu_termux_ai(self, prompt, ehdotus):
        """Yhdistää Termuxissa pyörivään Ollama-tekoälyyn käyttäen 1 kt paristoja kontekstina"""
        try:
            # Luetaan paristojen nykyinen raaka tila tekoälyn pohjaksi
            with open(self.f_bios1, "r", errors="ignore") as f: b1 = f.read().strip()
            with open(self.f_bios2, "r", errors="ignore") as f: b2 = f.read().strip()
            with open(self.f_bios3, "r", errors="ignore") as f: b3 = f.read().strip()

            # Rakennetaan tekoälylle tiivis järjestelmäohje paristojen arvot huomioiden
            komento_data = {
                "model": "tinydolphin", # Kepeä malli, joka sopii Termuxin resursseille
                "prompt": f"Konteksti paristoista:\nB1:{b1}\nB2:{b2}\nB3:{b3}\n\nEhdotus lukituksesta: {ehdotus}\nKäyttäjän syöte: {prompt}\n\nLuo lyhyt, tiivis tekoälyn reaktio linjan lukitukseen:",
                "stream": False
            }

            # Kutsutaan paikallista Ollama API:a curl-komennolla Termux-ympäristössä
            prosessointi = subprocess.Popen(
                ['curl', '-s', '-X', 'POST', 'http://localhost:11434/api/generate', '-d', json.dumps(komento_data)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, _ = prosessointi.communicate()
            vastauksen_json = json.loads(stdout.decode('utf-8'))
            return vastauksen_json.get("response", "Termux-yhteys virheetön, mutta vastaus tyhjä.")
        except Exception as e:
            # Jos tekoälyrauta ei ole päällä, palautetaan mekaaninen tila ilman virhettä
            return f"[Termux-AI Offline] Mekaaninen paristo syöttää varavastauksen."

    def aja_sykli(self, syote, viive_sekuntia):
        kuluneet_syklit = max(1, int(viive_sekuntia / self.sykli_kesto))
        timestamp = int(time.time())

        # 1. Kirjoitetaan kello-lokiin mekaaninen Hz-kulutus
        self._kirjoita_piiloloki(self.f_bios1, f"HZ:{self.hz}-CLK:{kuluneet_syklit}-TS:{timestamp}")

        # 2. Kirjoitetaan vahtilokiin rajapinnan tila
        self._kirjoita_piiloloki(self.f_bios2, f"MONITOR-VAL:{1000 - kuluneet_syklit}")

        # 3. Käsitellään sanat ja tallennetaan uudet ennakoitavat sanat BIOS 3 -lokiin
        sanat = syote.lower().split()
        vanhat_sanat = self.lue_sanavarasto()
        uudet_loydetyt = []

        for s in sanat:
            if s and s not in vanhat_sanat:
                # Tallennetaan piilokoodilla uusi sana 1 kt muistiin
                self._kirjoita_piiloloki(self.f_bios3, s)
                uudet_loydetyt.append(s)

        # Haetaan raudan vakiot ennustusta varten (jos ei uutta syötettä)
        vakiot = ["dna-ydin_1.1x10^-846", "4_950_000_euroa", "musta-neliö_teoria", "2.2_miljoonaa_henkilöä"]
        ehdotus = uudet_loydetyt[0] if uudet_loydetyt else random.choice(vakiot)

        # Tarkistetaan tiedostojen koot konsolissa (näet että ne ovat tasan 1 kt)
        b1_size = os.path.getsize(self.f_bios1)
        b2_size = os.path.getsize(self.f_bios2)
        b3_size = os.path.getsize(self.f_bios3)

        print(f"\n--- PARISTOJEN LOKITILA (Mekaaninen koko) ---")
        print(f"{self.f_bios1}: {b1_size} tavua (1 kt)")
        print(f"{self.f_bios2}: {b2_size} tavua (1 kt)")
        print(f"{self.f_bios3}: {b3_size} tavua (1 kt) <- Sanavarastosi")
        print(f"\nTallennetut uudet sanat tässä syklissä: {uudet_loydetyt}")

        # Kutsutaan Termux-tekoälyä prosessoimaan lukittu linja paristokontekstilla
        ai_vastaus = self._kutsu_termux_ai(syote, ehdotus)
        print(f"Termux-AI analyysi: {ai_vastaus}")

        return f"Ennakoiva editori lukitsee linjan: \"{ehdotus}\""

# --- KÄYTTÖ ---
editori = KilotavuEditori(hz=60)

print("=== 1 KT PARISTO-LOKI EDITORI LADATTU JÄRJESTELMÄÄN ===")
print("Yhdistetty Termux:in paikalliseen tekoälyrajapintaan.\n")

while True:
    alkuaika = time.time()
    kirjoitus = input("Kirjoita (tai 'sulje'): ")

    if kirjoitus.lower() == 'sulje':
        print("Tutkielma suljettu. Lokitiedostot säilötty paristoiksi.")
        break

    loppuaika = time.time()
    viive = loppuaika - alkuaika

    tulos = editori.aja_sykli(kirjoitus, viive)
    print(tulos)
    print("-" * 60)
