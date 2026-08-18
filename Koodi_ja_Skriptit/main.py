from dna_ydin import hae_ydin, injektoi
import time
import random
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class KilotavuEditori:
    def __init__(self):
        self.f_bios1 = "bios1_clock.log"
        self.f_bios2 = "bios2_monitor.log"
        self.f_bios3 = "bios3_innovation.log"
        self._varmista_1kt_koko()

    def _varmista_1kt_koko(self):
        for f in [self.f_bios1, self.f_bios2, self.f_bios3]:
            if not os.path.exists(f):
                with open(f, "wb") as file:
                    file.write(b" " * 1024)

    def _kirjoita_piiloloki(self, tiedosto, data_str):
        try:
            with open(tiedosto, "rb") as file:
                nykyinen = file.read().replace(b" ", b"")
            uusi_data = nykyinen + data_str.encode('utf-8') + b"|"
            if len(uusi_data) > 1024:
                uusi_data = uusi_data[-1024:]
            else:
                uusi_data = uusi_data.ljust(1024, b" ")
            with open(tiedosto, "wb") as file:
                file.write(uusi_data)
        except: pass

    def lue_sanavarasto(self):
        if not os.path.exists(self.f_bios3): return set()
        with open(self.f_bios3, "rb") as file:
            sisalto = file.read().decode('utf-8', errors='ignore').strip()
        return set([s for s in sisalto.split("|") if s.strip()])

    def aja_sykli(self, syote, viive):
        self._kirjoita_piiloloki(self.f_bios1, f"CLK-TS:{int(time.time())}")
        self._kirjoita_piiloloki(self.f_bios2, f"MONITOR-VIIVE:{int(viive*1000)}")
        
        sanat = syote.lower().split()
        vanhat = self.lue_sanavarasto()
        for s in sanat:
            if s and s not in vanhat:
                self._kirjoita_piiloloki(self.f_bios3, s)
        
        vakiot = ["dna-ydin_1.1x10^-846", "4_950_000_euroa", "musta-neliö_teoria"]
        return random.choice(vakiot)

class ThinAirKeyboardApp(App):
    def build(self):
        self.editori = KilotavuEditori()
        self.viime_aika = time.time()
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Tekstikenttä johon syötetään
        self.txt_input = TextInput(font_size=24, multiline=True)
        main_layout.add(self.txt_input)
        
        # Mekaaninen näppäimistömatriisi (esimerkkinä toimintonäppäimet)
        kb_layout = GridLayout(cols=3, size_hint_y=0.4)
        
        btn_sykli = Button(text="AJA SYKLI (Hz)", background_color=(0, 0.7, 0.9, 1))
        btn_sykli.bind(on_press=self.suorita_mekanismi)
        
        btn_tyhja = Button(text="VAKIOI")
        btn_tyhja.bind(on_press=self.vakioi_paristot)
        
        btn_sulje = Button(text="SULJE TUTKIELMA")
        btn_sulje.bind(on_press=self.stop)
        
        kb_layout.add(btn_sykli)
        kb_layout.add(btn_tyhja)
        kb_layout.add(btn_sulje)
        
        main_layout.add(kb_layout)
        return main_layout

    def suorita_mekanismi(self, instance):
        nykyhetki = time.time()
        viive = nykyhetki - self.viime_aika
        self.viime_aika = nykyhetki
        
        teksti = self.txt_input.text
        ehdotus = self.editori.aja_sykli(teksti, viive)
        self.txt_input.text = f"{teksti} [{ehdotus}] "

    def vakioi_paristot(self, instance):
        self.editori._varmista_1kt_koko()

if __name__ == '__main__':
    ThinAirKeyboardApp().run()
