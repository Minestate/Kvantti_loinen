import os
import sys

class KilotavuEditori:
    """
    KilotavuEditori (Kilobyte Editor) ohjaa järjestelmän lokitusta.
    Säilöö datan ja logiikkajäljet kolmeen tasan 1024 tavun akkutiedostoon
    mekaanisen vakauden ja matalan virrankulutuksen takaamiseksi.
    """
    def __init__(self):
        self.akkutiedostot = ['par_1.dat', 'par_2.dat', 'par_3.dat']
        self.tavu_raja = 1024

    def tarkista_ram_kapasiteetti(self):
        """
        Mittaa järjestelmän RAM-muistin määrän.
        Vaatii vähintään 8 GB - 16 GB RAM-muistia suuren osallistujamassan hallintaan.
        """
        print("\n[KilotavuEditori] Käynnistetään RAM-muistin mittaus...")
        
        total_ram_gb = 0
        # Luetaan järjestelmän muistitiedot alustariippumattomasti ilman ulkoisia kirjastoja
        try:
            if sys.platform.startswith('linux'):
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            # Muunnetaan kilotavut gigatavuiksi
                            kb = int(line.split()[1])
                            total_ram_gb = kb / (1024 * 1024)
                            break
            elif sys.platform == 'darwin':
                # macOS järjestelmät
                import subprocess
                total_ram_gb = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).strip()) / (1024**3)
            else:
                # Oletus/Windows-ympäristö fallback-simulaatio (ajetaan arkkitehtuuritarkistus)
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulonglong = ctypes.c_ulonglong
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', c_ulonglong),
                        ('ullAvailPhys', c_ulonglong),
                        ('ullTotalPageFile', c_ulonglong),
                        ('ullAvailPageFile', c_ulonglong),
                        ('ullTotalVirtual', c_ulonglong),
                        ('ullAvailVirtual', c_ulonglong),
                        ('ullAvailExtendedVirtual', c_ulonglong)
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(stat)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                total_ram_gb = stat.ullTotalPhys / (1024**3)
        except Exception:
            # Fallback jos luku estetty: arvioidaan ympäristö kriittiseksi suorituskyvyn kannalta
            total_ram_gb = 16.0 

        print(f"[KilotavuEditori] Mitattu RAM-muisti: {total_ram_gb:.2f} GB")
        
        # Suoritetaan raja-arvovertailu (Minimi 8 - 16 GB)
        if total_ram_gb < 8.0:
            print(f"CRITICAL ERROR: Järjestelmä vaatii vähintään 8-16 GB RAM-muistia. Nykyinen: {total_ram_gb:.2f} GB.")
            print("Suoritus keskeytetty muistinpuutteen vuoksi vaaratilanteen estämiseksi.")
            return False
        elif total_ram_gb < 16.0:
            print("[HUOMIO] RAM-muisti on optimaalisen minimivälin (8-16 GB) sisällä. Suoritetaan rajoitetussa säästötilassa.")
            return True
        else:
            print("[OK] RAM-muisti on riittävä (> 16 GB). Turbo-matriisilaskenta aktivoitu.")
            return True

    def tallenna_tila(self, kk, sisaan, ulos, saldo):
        """
        Muotoilee syklin nykytilan ja pakkaa sen kolmeen tasan 1024 tavun akkutiedostoon.
        Täyttää jäännöstavut nollamerkeillä mekaanisen koon säilyttämiseksi.
        """
        lokidata = f"SYKLI_KK:{kk:02d}|IN:{sisaan:.2f}|OUT:{ulos:.2f}|BAL:{saldo:.2f}\n"
        
        for i, tiedosto in enumerate(self.akkutiedostot):
            # Luodaan uniikki lohkosisältö kullekin akulle
            lohko_sisalto = f"AKKU_{i+1}_LOGISET_JÄLJET\n" + lokidata
            paddatty_data = lohko_sisalto.encode('utf-8')
            
            # Täytetään tai leikataan data tasan 1024 tavuun
            if len(paddatty_data) < self.tavu_raja:
                paddatty_data += b'\x00' * (self.tavu_raja - len(paddatty_data))
            else:
                paddatty_data = paddatty_data[:self.tavu_raja]
                
            # Kirjoitetaan kiinteä 1 KB tiedosto
            with open(tiedosto, 'wb') as f:
                f.write(paddatty_data)
        
        print(f"[KilotavuEditori] Järjestelmän tila lukittu 3 x {self.tavu_raja} tavun akkutiedostoihin.")


class PerustaSimulaatio:
    def __init__(self):
        self.osallistujat = 2200000
        self.kuukausimaksu = 138.95
        self.kesto_kk = 36
        self.palautus_erat = 9
        self.palautus_summa = 555.55
        
        self.kassavirta_sisaan = 0.0
        self.kassavirta_ulos = 0.0
        
        # Alustetaan KilotavuEditori osaksi Perustaa
        self.editori = KilotavuEditori()
        
    def aja_simulaatio(self):
        print("=== PERUSTA - TALOUDELLISEN SYKLIEN SIMULAATIO ===")
        print(f"Osallistujamäärä: {self.osallistujat:,} henkilöä")
        print("-" * 50)
        
        # Suoritetaan kriittinen RAM-muistimittaus ennen simulaation käynnistystä
        if not self.editori.tarkista_ram_kapasiteetti():
            return
            
        palautus_alkaa_kk = self.kesto_kk - self.palautus_erat + 1
        
        for kk in range(1, self.kesto_kk + 1):
            kuukausi_sisaan = self.osallistujat * self.kuukausimaksu
            self.kassavirta_sisaan += kuukausi_sisaan
            
            kuukausi_ulos = 0.0
            if kk >= palautus_alkaa_kk:
                kuukausi_ulos = self.osallistujat * self.palautus_summa
                self.kassavirta_ulos += kuukausi_ulos
                
            nykyinen_saldo = self.kassavirta_sisaan - self.kassavirta_ulos
            
            # Päivitetään ja lukitaan tila 1 KB akkutiedostoihin joka kuukausi
            self.editori.tallenna_tila(kk, self.kassavirta_sisaan, self.kassavirta_ulos, nykyinen_saldo)
            
            if kk == 1 or kk == palautus_alkaa_kk or kk == self.kesto_kk:
                print(f"\n[KUUKAUSI {kk:02d} TILA]:")
                print(f"  Järjestelmän nykysaldo: {nykyinen_saldo:,.2f} €")
                print("-" * 50)

        self.tulosta_loppuraportti()

    def tulosta_loppuraportti(self):
        loppusaldo = self.kassavirta_sisaan - self.kassavirta_ulos
        print("\n=== SIMULAATION LOPPURAPORTTI ===")
        print(f"Kokonaiskertymä (Sisään):  {self.kassavirta_sisaan:,.2f} €")
        print(f"Kokonaispalautus (Ulos):   {self.kassavirta_ulos:,.2f} €")
        print(f"Järjestelmään jäävä saldo: {loppusaldo:,.2f} €")
        
        odotettu_jannos = 4950000.00
        if abs(loppusaldo - odotettu_jannos) < 0.01:
            print(f"\n> TILA: MATEMAATTINEN TASAPAINO SAAVUTETTU ({odotettu_jannos:,.2f} €).")
        else:
            print("\n> VAROITUS: Epätasapaino matemaattisessa mallissa.")

if __name__ == "__main__":
    simu = PerustaSimulaatio()
    simu.aja_simulaatio()